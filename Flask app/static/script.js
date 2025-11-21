class VideoDownloader {
    constructor() {
        this.currentPlatform = "1"; // Default to YouTube
        this.currentUrl = "";
        this.currentDownloadId = null;
        this.progressInterval = null;
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Platform selection
        document.querySelectorAll('.platform-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.selectPlatform(e.target.dataset.platform);
            });
        });

        // Get video info
        document.getElementById('getInfoBtn').addEventListener('click', () => this.getVideoInfo());
        
        // Format selection
        document.querySelectorAll('.format-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.startDownload(e.target.dataset.format);
            });
        });
        
        // Download file button
        document.getElementById('downloadFileBtn').addEventListener('click', () => {
            this.downloadFile();
        });
        
        // Enter key for URL input
        document.getElementById('urlInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.getVideoInfo();
            }
        });
    }

    selectPlatform(platform) {
        this.currentPlatform = platform;
        
        // Update UI
        document.querySelectorAll('.platform-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-platform="${platform}"]`).classList.add('active');
        
        // Update placeholder text
        const urlInput = document.getElementById('urlInput');
        if (platform === "1") {
            urlInput.placeholder = "Enter YouTube URL...";
        } else {
            urlInput.placeholder = "Enter Instagram URL...";
        }
    }

    async getVideoInfo() {
        const url = document.getElementById('urlInput').value.trim();
        if (!url) {
            this.showError('Please enter a URL');
            return;
        }

        this.currentUrl = url;
        this.showLoading(true);
        this.hideError();

        try {
            const response = await fetch('/get_video_info', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    url: url,
                    platform: this.currentPlatform 
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to fetch video info');
            }

            this.displayVideoInfo(data);
            this.showFormatSelection();

        } catch (error) {
            this.showError(error.message);
        } finally {
            this.showLoading(false);
        }
    }

    displayVideoInfo(data) {
        const videoInfo = document.getElementById('videoInfo');
        const thumbnail = document.getElementById('thumbnail');
        const title = document.getElementById('videoTitle');
        const duration = document.getElementById('videoDuration');

        thumbnail.src = data.thumbnail || '/static/placeholder.jpg';
        thumbnail.alt = data.title;
        title.textContent = data.title;
        
        if (data.duration) {
            const minutes = Math.floor(data.duration / 60);
            const seconds = data.duration % 60;
            duration.textContent = `Duration: ${minutes}:${seconds.toString().padStart(2, '0')}`;
        }

        videoInfo.classList.remove('hidden');
    }

    showFormatSelection() {
        document.getElementById('formatSelection').classList.remove('hidden');
    }

    async startDownload(formatChoice) {
        if (!this.currentUrl) {
            this.showError('Please enter a URL first');
            return;
        }

        this.showLoading(true);
        this.hideError();

        try {
            const response = await fetch('/download', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    url: this.currentUrl,
                    platform: this.currentPlatform,
                    format_choice: formatChoice
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to start download');
            }

            this.currentDownloadId = data.download_id;
            this.showDownloadProgress();
            this.monitorDownloadProgress();

        } catch (error) {
            this.showError(error.message);
            this.showLoading(false);
        }
    }

    async monitorDownloadProgress() {
        const progressFill = document.getElementById('progressFill');
        const progressText = document.getElementById('progressText');
        const statusMessage = document.getElementById('statusMessage');
        const downloadBtn = document.getElementById('downloadFileBtn');

        this.progressInterval = setInterval(async () => {
            try {
                const response = await fetch(`/status/${this.currentDownloadId}`);
                const status = await response.json();

                if (status.status === 'completed') {
                    clearInterval(this.progressInterval);
                    progressFill.style.width = '100%';
                    progressText.textContent = '100%';
                    statusMessage.textContent = status.message || 'Download completed successfully!';
                    
                    // Show download button
                    downloadBtn.classList.remove('hidden');
                    downloadBtn.textContent = `Download ${status.filename || 'File'}`;
                    this.showLoading(false);
                    
                } else if (status.status === 'error') {
                    clearInterval(this.progressInterval);
                    this.showError(status.message || 'Download failed');
                    this.showLoading(false);
                } else if (status.status === 'downloading' || status.status === 'starting') {
                    const progress = status.progress || 0;
                    progressFill.style.width = `${progress}%`;
                    progressText.textContent = `${progress}%`;
                    statusMessage.textContent = status.message || 'Downloading...';
                }
            } catch (error) {
                console.error('Error checking progress:', error);
            }
        }, 1000);
    }

    downloadFile() {
        if (this.currentDownloadId) {
            // Open download in new tab
            window.open(`/download_file/${this.currentDownloadId}`, '_blank');
        }
    }

    showDownloadProgress() {
        const progressSection = document.getElementById('downloadProgress');
        progressSection.classList.remove('hidden');
        
        // Reset progress and hide download button
        document.getElementById('progressFill').style.width = '0%';
        document.getElementById('progressText').textContent = '0%';
        document.getElementById('statusMessage').textContent = 'Starting download...';
        document.getElementById('downloadFileBtn').classList.add('hidden');
    }

    showLoading(show) {
        const button = document.getElementById('getInfoBtn');
        if (show) {
            button.disabled = true;
            button.textContent = 'Processing...';
            document.body.classList.add('loading');
        } else {
            button.disabled = false;
            button.textContent = 'Get Video Info';
            document.body.classList.remove('loading');
        }
    }

    showError(message) {
        const errorDiv = document.getElementById('errorMessage');
        errorDiv.textContent = message;
        errorDiv.classList.remove('hidden');
    }

    hideError() {
        const errorDiv = document.getElementById('errorMessage');
        errorDiv.classList.add('hidden');
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    new VideoDownloader();
});