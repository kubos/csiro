## Verifying services on CSIRO board

- Modify `config.toml` to point to the local IP of the csiro board.
- Ensure python dependencies are installed with `pip install -r requirements.txt`.
- Service verification can be initiated two ways:
  - Verify all services with `pytest -v`.
  - Verify an individual service with `pytest -v test_service.py`.
- The service under test **must** already be running on the board prior to running the verification script.