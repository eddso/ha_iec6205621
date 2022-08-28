# IEC 62056-21 electricity meter Integration for Home-Assiatant

Custom integration for Home Assistant to connect electricity meter wia IEC 62056-21 protocol [mode B](https://github.com/lvzon/dsmr-p1-parser/blob/master/doc/IEC-62056-21-notes.md).

The integration polls every 5 minutes and provides 2 entities:
- Energy consumption total in kWh
- Energy feed total in kWh
