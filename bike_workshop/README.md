# Bike Workshop

## Description

Bike Workshop is a custom Odoo 19 module for managing bikes in a bike workshop.

The module allows authorized workshop staff to create, view, update, and delete bike records.

Each bike record contains information such as:

- Bike Name
- Brand
- Bike Type
- Purchase Date
- Last Maintenance Date
- Daily Rental Price
- Wheel Size

## Requirements

- Odoo 19 Community
- Python environment configured for Odoo
- PostgreSQL
- Access to the custom addons directory

## Installation

1. Place the `bike_workshop` module inside the Odoo custom addons directory.
2. Make sure the custom addons directory is included in the Odoo configuration file.
3. Start Odoo.
4. Open the Odoo Apps menu.
5. Enable Developer Mode if necessary.
6. Click **Update Apps List**.
7. Search for **Bike Workshop**.
8. Install the **Bike Workshop** module.

The module should install successfully without errors.

## Usage

After installation:

1. Open the **Bike Workshop** menu.
2. Open **Bikes**.
3. Create a new bike record.
4. Enter the required bike information.
5. Save the record.

Users with Workshop Staff permissions can manage bike records through the List and Form views.

## Bike Types

The module supports the following bike types:

- Road
- Mountain
- City
- Electric

## Security

A dedicated **Workshop Staff** security group is provided.

Only users assigned to the Workshop Staff group can manage bike records.

The Administrator user is assigned to the Workshop Staff group by default.

The access control list provides the following permissions to Workshop Staff:

- Read
- Write
- Create
- Delete

Users without the required permissions cannot access the Bike Workshop functionality.

## Testing

The module was tested on Odoo 19 Community.

The following items were verified:

- Successful module installation
- Successful module upgrade
- Successful creation of bike records
- Successful management of bike records
- List View
- Form View
- Bike Workshop menu
- Workshop Staff access permissions
- Administrator default access
- Unauthorized user restriction

No installation or upgrade errors were encountered during testing.س