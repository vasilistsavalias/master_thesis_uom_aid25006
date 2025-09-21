# src/thesis_pipeline/components/exploratory_data_analysis.py
import logging
import pandas as pd
from PIL import Image
from pathlib import Path
import matplotlib.pyplot as plt
from tqdm import tqdm

class ExploratoryDataAnalyzer:
    """
    Encapsulates the logic for performing EDA on a directory of images.
    """
    def __init__(self, input_dir: Path, output_dir: Path, extensions: list):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.extensions = extensions
        self.logger = logging.getLogger(__name__)
        self.df = None

    def _get_image_files(self) -> list:
        """Finds all image files with given extensions in the input directory."""
        image_files = []
        for ext in self.extensions:
            image_files.extend(self.input_dir.rglob(f'*{ext}'))
        self.logger.info(f"Found {len(image_files)} image files in {self.input_dir}.")
        return image_files

    def analyze_images(self, image_files: list):
        """Analyzes a list of image files and creates a DataFrame with metadata."""
        data = []
        self.logger.info("Analyzing image metadata...")
        for img_path in tqdm(image_files, desc="Analyzing Images"):
            try:
                with Image.open(img_path) as img:
                    width, height = img.size
                    data.append({
                        'filename': img_path.name,
                        'width': width,
                        'height': height,
                        'aspect_ratio': width / height if height > 0 else 0,
                        'mode': img.mode,
                        'filesize_kb': img_path.stat().st_size / 1024
                    })
            except Exception as e:
                self.logger.warning(f"Could not analyze image {img_path}. Error: {e}")
        
        self.df = pd.DataFrame(data)

    def generate_visualizations(self):
        """Generates and saves plots based on the image analysis DataFrame."""
        if self.df is None or self.df.empty:
            self.logger.warning("DataFrame is empty. Skipping visualization generation.")
            return

        plt.style.use('ggplot')
        
        # Plotting functions
        self._plot_histogram('width', 'skyblue', 'Width (pixels)')
        self._plot_histogram('height', 'salmon', 'Height (pixels)')
        self._plot_scatter('width', 'height', 'Image Dimensions (Width vs. Height)')
        self._plot_pie_chart()

        self.logger.info(f"All visualizations saved to: {self.output_dir}")

    def save_summary(self):
        """Saves summary statistics and the full metadata CSV."""
        if self.df is None or self.df.empty:
            self.logger.warning("DataFrame is empty. Skipping summary generation.")
            return
            
        # Summary Statistics
        summary_stats = self.df.describe()
        summary_path = self.output_dir / 'summary_statistics.txt'
        with open(summary_path, 'w') as f:
            f.write(f"Total Images Analyzed: {len(self.df)}\n\n{summary_stats.to_string()}")
        self.logger.info(f"Summary statistics saved to {summary_path}")

        # Full Metadata CSV
        csv_path = self.output_dir / 'full_image_metadata.csv'
        self.df.to_csv(csv_path, index=False)
        self.logger.info(f"Full metadata saved to {csv_path}")

    def run(self):
        """Executes the full EDA process."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        image_files = self._get_image_files()
        if not image_files:
            self.logger.warning("No image files found. EDA concluded.")
            return
        
        self.analyze_images(image_files)
        self.generate_visualizations()
        self.save_summary()

    # --- Helper plotting methods ---
    def _plot_histogram(self, column, color, xlabel):
        plt.figure(figsize=(12, 6))
        plt.hist(self.df[column], bins=50, color=color, edgecolor='black')
        plt.title(f'Distribution of Image {column.title()}s')
        plt.xlabel(xlabel)
        plt.ylabel('Frequency')
        plt.savefig(self.output_dir / f'{column}_distribution.png')
        plt.close()

    def _plot_scatter(self, x_col, y_col, title):
        plt.figure(figsize=(10, 10))
        plt.scatter(self.df[x_col], self.df[y_col], alpha=0.6, edgecolors='w', s=50)
        plt.title(title)
        plt.xlabel(f'{x_col.title()} (pixels)')
        plt.ylabel(f'{y_col.title()} (pixels)')
        plt.savefig(self.output_dir / 'dimensions_scatter_plot.png')
        plt.close()

    def _plot_pie_chart(self):
        plt.figure(figsize=(8, 8))
        self.df['extension'] = self.df['filename'].apply(lambda x: Path(x).suffix.lower())
        ext_counts = self.df['extension'].value_counts()
        ext_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90)
        plt.title('Distribution of Image File Formats')
        plt.ylabel('')
        plt.savefig(self.output_dir / 'file_format_distribution.png')
        plt.close()
