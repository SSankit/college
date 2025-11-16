frappe.ui.form.on("Enrolment", {

    onload: function (frm) {
        if (frm.is_new()) {
            frm.set_intro("Course Enrollment is open only for 3 more days");
        }
    },

    // When a Course is selected, try to fetch its numeric fee if course_fees isn't numeric
    course: function (frm) {
        // If course_fees is missing or not numeric, fetch from Course doctype
        const cf = frm.doc.course_fees;
        if (frm.doc.course && (!cf || isNaN(Number(cf)))) {
            frappe.db.get_value('Course', frm.doc.course, 'course_fees').then(r => {
                const val = r && r.message && r.message.course_fees ? Number(r.message.course_fees) : 0;
                frm.set_value('course_fees', val);
                frm.trigger('calculate_total');
            });
        } else {
            frm.trigger('calculate_total');
        }
    },

    // Trigger when Course Fees changes
    course_fees: function (frm) {
        frm.trigger("calculate_total");
    },

    // Trigger when Registration Fees changes
    registration_fees: function (frm) {
        frm.trigger("calculate_total");
    },

    // Function to calculate total fees
    calculate_total: function (frm) {
        const course_fees = Number(frm.doc.course_fees) || 0;
        const reg_fees = Number(frm.doc.registration_fees) || 0;

        const total = course_fees + reg_fees;
        frm.set_value("total_fees", total);
    },

    validate: function (frm) {
        const sem = frm.doc.semester || 0;

        if (sem > 4) {
            frappe.throw("Students above Semester 4 are not allowed to enroll.");
        }
    }
});
