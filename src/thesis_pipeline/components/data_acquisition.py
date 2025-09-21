# src/thesis_pipeline/components/data_acquisition.py
import requests
import logging
from pathlib import Path
from tqdm import tqdm

class DataAcquisition:
    def __init__(self, api_url: str):
        self.api_url = api_url
        self.session = requests.Session()
        self.logger = logging.getLogger(__name__)

    def _get_images_in_category_recursive(self, category: str, visited_categories: set):
        """Recursively fetches image file information from a Wikimedia category."""
        if category in visited_categories:
            return []
        visited_categories.add(category)
        
        images = []
        params = {
            "action": "query",
            "format": "json",
            "list": "categorymembers",
            "cmtitle": category,
            "cmlimit": "500",
            "cmtype": "file|subcat"
        }
        
        try:
            response = self.session.get(url=self.api_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            members = data.get("query", {}).get("categorymembers", [])
            
            for member in members:
                if member["ns"] == 6:  # Namespace 6 is for files
                    images.append(member["title"])
                elif member["ns"] == 14:  # Namespace 14 is for subcategories
                    images.extend(self._get_images_in_category_recursive(member["title"], visited_categories))

        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch category {category}: {e}")

        return images

    def _download_image(self, image_title: str, output_dir: Path):
        """Downloads a single image."""
        params = {
            "action": "query",
            "format": "json",
            "titles": image_title,
            "prop": "imageinfo",
            "iiprop": "url"
        }
        try:
            response = self.session.get(url=self.api_url, params=params)
            response.raise_for_status()
            data = response.json()
            pages = data.get("query", {}).get("pages", {})
            
            for page_id in pages:
                if "imageinfo" in pages[page_id]:
                    image_url = pages[page_id]["imageinfo"][0]["url"]
                    # Sanitize filename
                    image_name = "".join(c for c in Path(image_url).name if c.isalnum() or c in ('.', '_')).rstrip()
                    output_path = output_dir / image_name
                    
                    if not output_path.exists():
                        img_response = self.session.get(image_url, stream=True)
                        img_response.raise_for_status()
                        with open(output_path, "wb") as f:
                            for chunk in img_response.iter_content(chunk_size=8192):
                                f.write(chunk)
                        return True
        except requests.RequestException as e:
            self.logger.error(f"Failed to download image {image_title}: {e}")
        return False

    def download_images_from_category(self, start_category: str, output_dir: Path, limit: int):
        """
        Downloads images from a starting Wikimedia category and its subcategories.
        """
        self.logger.info("Fetching list of all images in category tree...")
        all_images = list(set(self._get_images_in_category_recursive(start_category, set())))
        self.logger.info(f"Found {len(all_images)} total unique images.")

        if not all_images:
            self.logger.warning("No images found in the specified category tree.")
            return

        images_to_download = all_images[:limit]
        self.logger.info(f"Attempting to download up to {len(images_to_download)} images.")

        output_dir.mkdir(parents=True, exist_ok=True)
        
        download_count = 0
        for image_title in tqdm(images_to_download, desc="Downloading Images"):
            if self._download_image(image_title, output_dir):
                download_count += 1
        
        self.logger.info(f"Successfully downloaded {download_count} new images to {output_dir}")
