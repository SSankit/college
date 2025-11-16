# Copyright (c) 2025, IDML and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document

class Enrolment(Document):

    def validate(self):
        """Seat checking before saving"""

        if not self.course:
            frappe.throw("Please select a Course first.")

        # Show Course ID only
        frappe.msgprint("Server Script Started...")
        frappe.msgprint(f"Selected Course ID: {self.course}")

        try:
            # Fetch seats from Course Doctype (using Course ID)
            total_seats = frappe.db.get_value("Course", self.course, "total_seats")
            available_seats = frappe.db.get_value("Course", self.course, "available_seats")

            frappe.msgprint(f"Total Seats: {total_seats}")
            frappe.msgprint(f"Available Seats: {available_seats}")

            # Validate seats exist
            if total_seats is None or available_seats is None:
                frappe.throw("Course seats fields are missing in Course doctype.")

            total_seats = int(total_seats)
            available_seats = int(available_seats)

            # If no seats → stop enrollment
            if available_seats <= 0:
                frappe.throw(
                    f"No seats available for Course ID <b>{self.course}</b>.<br>"
                    f"Available Seats: <b>{available_seats}</b>",
                    title="Course Full"
                )

            # Deduct seat
            new_available = available_seats - 1
            frappe.db.set_value("Course", self.course, "available_seats", new_available)

            frappe.msgprint(
                f"Enrollment Successful! Remaining Seats for Course ID {self.course}: {new_available}"
            )

        except Exception as e:
            frappe.msgprint(f"Error: {e}")
            frappe.log_error("Enrollment Seat Update Error", str(e))
