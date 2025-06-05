# API Rate Limiter - System Design

## Generating the AWS System Design Diagram

This project includes a Graphviz DOT file (`system_design_aws.dot`) that describes the AWS architecture for the API rate limiter. You can generate a PNG image from this DOT file using Graphviz.

### 1. Install Graphviz

On Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install graphviz
```

On MacOS (with Homebrew):
```bash
brew install graphviz
```

### 2. Generate the PNG Diagram

From the `apiratelimiter` directory (or project root):
```bash
dot -Tpng system_design_aws.dot -o system_design_aws.png
```

### 3. View the PNG Image

You can open the generated `system_design_aws.png` file with any image viewer, for example:

On Ubuntu:
```bash
eog system_design_aws.png
```

On MacOS:
```bash
open system_design_aws.png
```

Or simply double-click the file in your file browser.

---

For any changes to the architecture, edit the DOT file and re-run the above command to regenerate the diagram. 