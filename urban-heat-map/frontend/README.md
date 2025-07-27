# Urban Heat Map Frontend

This project is a frontend application for the Urban Heat Map, built using React and TypeScript. It interfaces with a backend service to fetch and display temperature data on a map.

## Project Structure

- **public/index.html**: The main HTML file that serves as the entry point for the application.
- **src/App.tsx**: The main application component that sets up the overall structure of the app.
- **src/index.tsx**: The entry point for the React application, rendering the `App` component.
- **src/components/MapView.tsx**: A component responsible for displaying the map and fetching tiles from the backend.
- **src/styles/App.css**: CSS styles for the application, defining the visual appearance of the components.
- **tsconfig.json**: TypeScript configuration file specifying compiler options.
- **package.json**: npm configuration file listing dependencies and scripts.

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd urban-heat-map/frontend
   ```

2. **Install dependencies**:
   ```
   npm install
   ```

3. **Run the application**:
   ```
   npm start
   ```

4. Open your browser and navigate to `http://localhost:3000` to view the application.

## Usage

The application displays a map with temperature tiles fetched from the backend service. You can interact with the map to view temperature data for different regions.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.