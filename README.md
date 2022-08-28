# IEC 62056-21 electricity meter Integration for Home-Assiatant

Custom integration for Home Assistant to connect electricity meter wia IEC 62056-21 protocol [mode B](https://github.com/lvzon/dsmr-p1-parser/blob/master/doc/IEC-62056-21-notes.md).

The integration polls every 5 minutes and provides 2 entities:
- Energy consumption total in kWh
- Energy feed total in kWh

## Installation
### a) Install over HACS
- Add `https://github.com/eddso/https://github.com/eddso/ha_iec6205621` repository to HACS integrations
- Add `IEC 62056-21 electricity meter Integration` integration with HACS
### b) Install manual
If you don't have or don't want use HACS, install it over Terminal:
```
cd config/custom_components
wget https://github.com/eddso/ha_iec6205621/archive/refs/heads/main.tar.gz
tar --strip-components=3 -xzf main.tar.gz ha_sma_speedwire-main/custom_components/sma_speedwire
```
### Restart 
After install restart Home-Assistant under the  Configuration -> System -> Restart

## Setup
- After installation, you should find **iec6205621** under the Configuration -> Integrations -> Add integration.
- Enter serial port connected to electricity meter.

## Debugging
Add the following to `configuration.yml` to show debugging logs. Please make sure to include debug logs when filing an issue.

See [logger intergration docs](https://www.home-assistant.io/integrations/logger/) for more information to configure logging.

```yml
logger:
  default: warning
  logs:
    custom_components.iec6205621: debug
```
