# Bike Workshop

## Description

Bike Workshop is a custom Odoo 19 Community module for managing bikes, rentals, repairs, spare parts, and related workshop operations.

The module allows authorized workshop staff to manage bike records, rental operations, repair jobs, spare parts, customer information, and service information.

## Features

### Bike Management

Each bike record contains:

* Bike Name
* Brand
* Bike Type
* Purchase Date
* Last Maintenance Date
* Daily Rental Price
* Wheel Size
* Assigned Mechanic
* Last Service Date
* Service Notes

Supported bike types:

* Road
* Mountain
* City
* Electric

A Rental Count smart button is available on the Bike form to view the rental history of each bike.

### Rental Management

The rental system supports:

* Unique Rental Reference
* Customer
* Rented Bike
* Rental Start Date
* Expected Return Date
* Actual Return Date
* Daily Rental Price
* Rental Duration
* Total Rental Amount

The daily rental price is automatically populated from the selected bike.

Rental duration is calculated automatically from the rental dates.

The total rental amount is calculated as:

`Rental Duration × Daily Rental Price`

Existing rental prices remain independent from later changes to the bike's rental price.

### Rental Lifecycle

The rental workflow is:

`Draft → Confirmed → Returned`

* New rentals start in Draft.
* Only Draft rentals can be confirmed.
* Only Confirmed rentals can be returned.
* Returning a rental automatically sets the Actual Return Date to the current date.
* Returned rentals cannot be processed again.
* Expected Return Date must be after Rental Start Date.
* Invalid rental dates are rejected through data-level validation.
* Rental duration must be greater than zero.
* Daily rental price and total rental amount cannot be negative.

### Rental Conflict Prevention

The system prevents conflicting rentals during confirmation.

A rental cannot be confirmed when:

* The same bike has another Confirmed Rental overlapping the selected rental period.
* The selected workshop bike has an In Progress Repair.

Draft and Returned rentals do not block new rentals.

Non-overlapping rental periods are allowed.

Once a repair is Completed or Cancelled, the workshop bike becomes eligible for future rental confirmation.

### Repair Management

The repair system supports both:

* Workshop Bikes
* External Customer Bikes

Repair records contain:

* Unique Repair Reference
* Customer
* Bike Source
* Workshop Bike when applicable
* External Bike Reference
* External Bike Brand
* External Bike Type
* Reported Issue
* Assigned Mechanic
* Last Service Date
* Service Notes
* Total Spare Parts Cost

External bikes are handled separately and do not automatically become part of the workshop's rentable bike fleet.

### Repair Lifecycle

The repair workflow is:

`Draft → In Progress → Completed`

Cancellation is available from Draft and In Progress.

* Only Draft repairs can be started.
* Starting a repair requires the required customer, issue, mechanic, and bike information.
* Only In Progress repairs can be completed.
* Completing a repair requires Service Notes and Last Service Date.
* Draft and In Progress repairs can be cancelled.
* Completed and Cancelled repairs cannot be processed again.

### Spare Parts

Repair spare parts use Odoo Products instead of a separate spare-parts catalog.

Products can be marked using the:

`Spare Part`

indicator.

Only products marked as Spare Parts can be selected in Repair spare-part lines.

Each repair can contain multiple spare-part lines with:

* Product
* Quantity
* Unit Price
* Subtotal

The Unit Price is initially populated from the selected Odoo Product.

The Subtotal is calculated as:

`Quantity × Unit Price`

The Total Spare Parts Cost is calculated as the sum of all spare-part subtotals.

Quantity and pricing values cannot be negative.

Existing repair line prices remain independent from later changes to the product price.

### Shared Service Information

A reusable service information mixin is shared by Bikes and Repairs.

The shared information includes:

* Assigned Mechanic
* Last Service Date
* Service Notes

This avoids duplicating the same fields and allows future workshop models to reuse the same service information.

### Customer Information

The standard Odoo `res.partner` model is extended with:

* Preferred Bike Type

The available options are:

* Road
* Mountain
* City
* Electric

The existing Contacts form is extended using Odoo view inheritance.

## Views and Navigation

The module provides:

* List Views
* Form Views
* Search Views
* Search Filters
* Workflow Buttons
* Status Indicators
* Smart Buttons
* Bike Menu
* Rental Menus
* Repair Menu

Rental navigation includes:

* All Rentals
* Confirmed Rentals

The Bike Rental smart button provides filtered rental history for the selected bike.

## Security

A dedicated `Workshop Staff` security group is provided.

Workshop Staff have access to manage:

* Bikes
* Rentals
* Repairs
* Repair Spare Parts

The Administrator user is assigned to the Workshop Staff group by default.

The access control list provides:

* Read
* Write
* Create
* Delete

Users without the required permissions cannot access the Bike Workshop functionality.

## Requirements

* Odoo 19 Community
* Python environment configured for Odoo
* PostgreSQL
* Access to the custom addons directory

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
2. Use **Bikes** to manage workshop bikes.
3. Use **Rentals** to create and manage bike rentals.
4. Use **Repairs** to manage workshop and external bike repairs.
5. Mark relevant Odoo Products as **Spare Parts** before using them in repairs.
6. Use the Bike Rental smart button to view rental history for a specific bike.

Users with Workshop Staff permissions can manage the available workshop operations through the List and Form views.

## Testing

The module was tested on Odoo 19 Community.

The following functionality was verified:

* Successful module installation
* Successful module upgrade
* Bike creation and management
* Bike List, Form, and Search Views
* Rental creation
* Automatic rental reference generation
* Rental price auto-fill from Bike
* Rental duration calculation
* Total rental amount calculation
* Rental date changes and recalculation
* Invalid rental date validation
* Rental Draft → Confirmed → Returned workflow
* Automatic actual return date
* Rental overlap detection
* Rental and Repair conflict prevention
* Repair creation
* Automatic repair reference generation
* Workshop Bike repairs
* External Bike repairs
* Repair Draft → In Progress → Completed workflow
* Repair cancellation
* Repair validation
* Spare Part product identification
* Spare Part product filtering in repairs
* Spare-part price auto-fill
* Spare-part subtotal calculation
* Total spare-parts cost calculation
* Spare-parts validation
* Shared Service Information
* Preferred Bike Type on Contacts
* Bike rental smart button
* Filtered rental history
* All Rentals menu
* Confirmed Rentals menu
* Workshop Staff access permissions
* Unauthorized user restriction
* Existing Bike Workshop functionality from Exercise 1

No installation or upgrade errors were encountered during testing.
