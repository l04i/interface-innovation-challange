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
git clone https://github.com/l04i/battery-system-modeler.git
cd battery-system-modeler
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:

```bash
python main.py
```

2. Configure project settings:

   - Enter project name
   - Specify file name
   - Set operational limits
   - Configure dispatch control parameters

3. Run simulation:
   - Click "Run" button
   - Wait for process completion
   - Access generated reports and CSVs

## Directory Structure

```
battery-system-modeler/
├── main.py
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

## Development

### Adding New Features

1. Create new frame class inheriting from `BaseFrame`
2. Implement `_create_widgets` method
3. Add new constants to `Constants` class if needed
4. Update main application to include new frame

### Style Customization

1. Add new styles to `StyleManager`
2. Update constants in `Constants` class
3. Apply new styles to widgets

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

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
