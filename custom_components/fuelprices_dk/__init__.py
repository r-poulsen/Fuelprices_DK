from __future__ import annotations

import logging

from .fuelprices_dk_api import fuelprices

from .const import (
	DOMAIN,
	CONF_CLIENT,
	CONF_FUELCOMPANIES,
	CONF_FUELTYPES,
	CONF_PLATFORM,
)

_LOGGER: logging.Logger = logging.getLogger(__package__)
_LOGGER = logging.getLogger(__name__)


async def async_setup(hass, config):
	# Get the configuration
	conf = config.get(DOMAIN)
	# If no config, abort
	if conf is None:
		return True

	# Extract companies and fuueltypes from the config, defult to empty list
	fuelCompanies = conf.get(CONF_FUELCOMPANIES, [])
	fuelTypes = conf.get(CONF_FUELTYPES, [])

	# Initialize a instance of the fuelprices API
	fuelPrices = fuelprices()
	# Load the data using the config
	fuelPrices.loadCompanies(fuelCompanies, fuelTypes)
	# Store the client in the hass data stack
	hass.data[DOMAIN] = {CONF_CLIENT: fuelPrices}

	# Add sensors
	hass.async_create_task(
		hass.helpers.discovery.async_load_platform(CONF_PLATFORM, DOMAIN, conf, config)
	)

	# Initialization was successful.
	return True