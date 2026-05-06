import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

class KMeansCompressor:
    def __init__(self, n_clusters=16, max_iters=10):
        self.n_clusters = n_clusters
        self.max_iters = max_iters
        self.means = None
        self.index = None

    def read_image(self, image_path):
        """Membaca gambar dan normalisasi nilai pixel ke range 0-1."""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"File {image_path} tidak ditemukan.")
        img = mpimg.imread(image_path)
        # Normalisasi agar nilai pixel berada di antara 0 dan 1
        return img / 255.0

    def initialize_means(self, points):
        """Inisialisasi centroid secara acak dari titik data yang ada."""
        m, n = points.shape
        # Mengambil indeks acak unik sebanyak jumlah cluster
        random_indices = np.random.choice(m, self.n_clusters, replace=False)
        self.means = points[random_indices]

    def fit(self, points):
        """Menjalankan algoritma K-Means."""
        m, n = points.shape
        self.initialize_means(points)
        
        for i in range(self.max_iters):
            # Menghitung jarak Euclidean secara vektorisasi (lebih cepat dari loop)
            # distances shape: (jumlah_pixel, jumlah_cluster)
            distances = np.linalg.norm(points[:, np.newaxis] - self.means, axis=2)
            
            # Menentukan cluster terdekat untuk setiap pixel
            self.index = np.argmin(distances, axis=1)

            # Memperbarui posisi centroid (means)
            new_means = np.array([points[self.index == k].mean(axis=0) 
                                 if len(points[self.index == k]) > 0 
                                 else self.means[k] 
                                 for k in range(self.n_clusters)])
            
            # Cek konvergensi (jika centroid tidak berubah lagi)
            if np.all(self.means == new_means):
                print(f"Konvergensi tercapai pada iterasi ke-{i+1}")
                break
                
            self.means = new_means
            print(f"Iterasi {i+1}/{self.max_iters} selesai.")

    def compress(self, img_shape):
        """Mengonstruksi ulang gambar menggunakan centroid yang telah dipelajari."""
        recovered = self.means[self.index.astype(int), :]
        # Kembalikan ke bentuk matrix 3D original
        recovered = np.reshape(recovered, img_shape)
        return recovered

def main():
    filename = 'Harimau.jpg' # Menggunakan gambar harimau sesuai permintaan
    
    try:
        # 1. Load Gambar
        compressor = KMeansCompressor(n_clusters=16, max_iters=10)
        img = compressor.read_image(filename)
        
        # 2. Reshape gambar menjadi daftar pixel (2D array)
        points = np.reshape(img, (img.shape[0] * img.shape[1], img.shape[2]))
        
        # 3. Jalankan K-Means
        print(f"Memulai kompresi gambar {filename}...")
        compressor.fit(points)
        
        # 4. Rekonstruksi Gambar
        compressed_img = compressor.compress(img.shape)
        
        # 5. Tampilkan dan Simpan Hasil
        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.title("Original")
        plt.imshow(img)
        plt.axis('off')

        plt.subplot(1, 2, 2)
        plt.title(f"Compressed ({compressor.n_clusters} Colors)")
        plt.imshow(compressed_img)
        plt.axis('off')
        
        output_name = f'compressed_harimau_{compressor.n_clusters}.png'
        plt.imsave(output_name, compressed_img)
        print(f"Hasil disimpan sebagai {output_name}")
        plt.show()

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

if __name__ == '__main__':
    main()