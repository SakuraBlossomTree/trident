# Trident

Trident is a lightweight UCI-compatible chess engine written in Python. It was developed as a small project to explore chess engine programming, search algorithms, and the Universal Chess Interface (UCI) protocol.

The engine uses an iterative deepening search with time-based limits, allowing it to make decisions within a specified time interval while remaining compatible with UCI-supported chess GUIs.

## Features

* UCI (Universal Chess Interface) compatible
* Written entirely in Python
* Iterative deepening search
* Time-based move calculation
* Compatible with popular chess GUIs
* Lightweight and easy to understand

## Screenshots

Screenshots and engine analysis examples will be added in a future update.

## Installation

Clone the repository:

```bash id="2nq7kj"
git clone https://github.com/yourusername/trident.git
cd trident
```

Install the required dependencies:

```bash id="w2krf5"
pip install -r requirements.txt
```

Run the engine:

```bash id="ab93mx"
python main.py
```

To use Trident with a chess GUI, add the Trident.bat executable through your preferred UCI-compatible interface.

## Built With

* Python
* UCI (Universal Chess Interface)

## Project Structure

```text id="h91lqv"
Trident/
├── engine/
├── search/
├── evaluation/
├── main.py
├── requirements.txt
└── README.md
```

## Design Goals

Trident was created as a learning project to better understand how chess engines work. The focus is on maintaining a clean and readable codebase while implementing the core components of a functional UCI chess engine.

Rather than competing with advanced engines, Trident emphasizes simplicity, experimentation, and educational value.

## Roadmap

* Add transposition tables
* Implement move ordering heuristics
* Support opening books
* Improve endgame play
* Add benchmarking tools

## Contributing

Contributions, bug reports, and suggestions are welcome. Feel free to open an issue or submit a pull request.

## License

This project is MIT licensed
