import frappe

def run_test():
    """Create or update a Course and run validate/on_submit on a transient Enrolment doc.
    Prints results to stdout for bench execute to capture.
    """
    course_name = 'Java Programming-0011'
    if not frappe.db.exists('Course', course_name):
        frappe.get_doc({
            'doctype': 'Course',
            'name': course_name,
            'course_name': 'Java Programming',
            'course_fees': 1000,
            'available_seats': 3
        }).insert(ignore_permissions=True)
        print('Created Course', course_name)
    else:
        frappe.db.set_value('Course', course_name, 'available_seats', 3)
        print('Course exists; reset available_seats to 3')

    en = frappe.get_doc({'doctype': 'Enrolment', 'course': course_name, 'registration_fees': 500})
    print('Prepared Enrolment doc (not inserted)')

    try:
        en.run_method('validate')
        print('validate() succeeded')
    except Exception as e:
        print('validate() raised:', repr(e))
        raise

    try:
        en.run_method('on_submit')
        print('on_submit() succeeded')
        rem = frappe.db.get_value('Course', course_name, 'available_seats')
        print('Remaining seats after on_submit():', rem)
    except Exception as e:
        print('on_submit() raised:', repr(e))
        raise

    return 'OK'
