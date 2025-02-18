# SecScanX

**SecScanX** is an advanced cybersecurity tool designed to automate the process of subdomain enumeration, URL discovery, and port scanning. This tool is essential for vulnerability assessment, security audits, and educational purposes in network security.

## Features

- **Subdomain Enumeration**: Automatically discover subdomains of a target domain using an external API.
- **URL Discovery**: Crawl the website to discover all URLs belonging to the domain.
- **Port Scanning**: Scan open ports for each discovered URL using a multi-threaded approach for efficiency.
- **Beautiful Terminal Output**: Provide informative and visually appealing terminal output with colored and bold text.
- **Error Handling**: Comprehensive error handling for network requests and socket operations.
- **Concurrency**: Use a thread pool to manage threads efficiently, improving performance.

## Installation

### Prerequisites

- Python 3.x
- Virtual environment (recommended)

### Setup

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/garybadwal/SecScanX.git
   cd SecScanX
   ```

2. **Create a Virtual Environment**:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   - Create a `.env` file in the project root.
   - Add your SecurityTrails API key to the `.env` file:
     ```
     API_KEY=your_securitytrails_api_key
     ```

## Usage

1. **Run the Script**:
   ```sh
   python secscanx.py
   ```

2. **Enter the Target Domain**:
   - When prompted, enter the target domain or IP address you want to scan.

3. **View the Output**:
   - The script will provide real-time updates in the terminal with colored and bold text, indicating the progress and results of the scanning process.

## Example

```sh
Enter target domain or IP: example.com
2023-10-01 12:34:56 - INFO - Found 230 subdomains for example.com
2023-10-01 12:34:57 - INFO - Scanning subdomain: https://subdomain1.example.com
2023-10-01 12:34:58 - INFO - Found 50 URLs for https://subdomain1.example.com
2023-10-01 12:34:59 - INFO - Scanning https://subdomain1.example.com for open ports...
2023-10-01 12:35:00 - INFO - Port 80 is OPEN on https://subdomain1.example.com
...
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature- branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Special thanks to the creators of the libraries and tools used in this project.
- Inspired by the need for automated and efficient cybersecurity tools.

---

**SecScanX** is designed to be a powerful and user-friendly tool for cybersecurity professionals. Use it responsibly and ethically to enhance your network security and stay ahead of potential threats.