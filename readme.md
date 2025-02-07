# Battery System Modeler - Interface Innovation Challenge

A Python-based GUI application developed for the Interface Innovation Challenge that implements a battery system modeling interface using tkinter.

## Technical Details

### Architecture

The application follows a modular architecture with separate frames for different functionalities:

- `BatteryModelerApp`: Main application window
- `ScrollableFrame`: Custom scrollable container
- `ProjectInfoFrame`: Project metadata management
- `OperationalLimitsFrame`: Battery limits configuration
- `DispatchControlFrame`: Dispatch settings
- `SystemConfigurationFrame`: System visualization
- `ActionFrame`: Control buttons and operations

## Installation

1. Clone the repository:

```bash
git clone https://github.com/l04i/interface-innovation-challange.git
cd interface-innovation-challange
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Start the application:

```bash
python main.py
```

## Directory Structure

```
battery-system-modeler/
├── main.py
|___app.py
├── config/
│   ├── constants.py
│   └── styles.py
├── widgets/
│   ├── base.py
│   └── frames.py
├── imgs/
│   ├── image.png
│   ├── success.png
│   ├── system.png
│   └── thumb.png
└── requirements.txt
```

## Error Handling

The application includes comprehensive error handling for:

- Invalid input validation
- File operations
- Image loading
- Process execution

## Dependencies

Major dependencies include:

- tkinter
- customtkinter
- Pillow
- threading
