# frc-py
Caching library and wrapper for [tbapy](https://github.com/frc1418/tbapy) and [Statbotics](https://github.com/avgupta456/statbotics).

The main goals of this library are as follows:
1. Harmonize TBA's API with Statbotics' such that the difference is transparent.
2. Cache API responses locally to assist in large requests.

The caching functionality is fully configurable, and by default caches team info for 280 days, and team stats for 7 days.
