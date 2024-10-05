/** @odoo-module **/

import dom from "@web/legacy/js/core/dom";
import publicWidget from "@web/legacy/js/public/public_widget";
import { findInvalidEmailFromText } from  "./utils.js"
import { _t } from "@web/core/l10n/translation";

publicWidget.registry.appointmentForm = publicWidget.Widget.extend({
    selector: '.o_appointment_attendee_form',
    events: {
        'click div.o_appointment_add_guests button.o_appointment_input_guest_add': '_onAddGuest',
        'click div.o_appointment_add_guests button.o_appointment_input_guest_cancel': '_onHideGuest',
        'click .o_appointment_form_confirm_btn': '_onConfirmAppointment',
        'click .custom-check-patient': 'async _onClickCheckPatient',
        'input #custom-patient-code': 'async _onChangePatientCode',
    },
    init() {
        this._super(...arguments);
        this.orm = this.bindService("orm");
        this.notification = this.bindService("notification");
    },
    start(){
        this.$patient_id = this.$('.custom-patient-id').first()[0];
        this.$code = this.$('.custom-patient-code').first()[0];
        this.$name = this.$('.custom-patient-name').first()[0];
        this.$email = this.$('.custom-patient-email').first()[0];
        this.$phone = this.$('.custom-patient-phone').first()[0];
    },
    _onChangePatientCode: async function(e){
        this._removePatientData({}, false)
    },
    _removePatientData: function({
        id=0,
        name='',
        email='',
        phone=''
    }, readOnly){
        this.$name.readOnly = readOnly;
        this.$email.readOnly = readOnly;
        this.$phone.readOnly = readOnly;
        this.$patient_id.value = id;
        this.$name.value = name;
        this.$email.value = email;
        this.$phone.value = phone;
    },
    _onClickCheckPatient: async function(){
        const res = await this.orm.call('res.partner', 'get_patient_by_code', [null, this.$code.value]);
        if (!res.id){
            this._removePatientData({}, false);
            this.notification.add(`Patient Code ${code.value} not found.`, { type: "danger"});
            return
        }
        this._removePatientData(res, true);
        const noti = this.notification.add(`Patient Code ${code.value} found.`, { type: "success"});
        console.log(noti);
    },
    /**
     * This function will show the guest email textarea where user can enter the
     * emails of the guests if allow_guests option is enabled.
     */
    _onAddGuest: function(){
        const textArea = this.el.querySelector('#o_appointment_input_guest_emails');
        textArea.classList.remove('d-none');
        textArea.focus();
        const addGuestDiv = this.el.querySelector('div.o_appointment_add_guests')
        addGuestDiv.querySelector('button.o_appointment_input_guest_add').classList.add('d-none')
        addGuestDiv.querySelector('button.o_appointment_input_guest_cancel').classList.remove('d-none')
    },

    _onConfirmAppointment: async function(event) {
        this._validateCheckboxes();
        const textArea = this.el.querySelector('#o_appointment_input_guest_emails');
        const appointmentForm = document.querySelector('.appointment_submit_form');
        if (textArea && textArea.value.trim() !== '') {
            let emailInfo = findInvalidEmailFromText(textArea.value);
            if (emailInfo.invalidEmails.length || emailInfo.emailList.length > 10) {
                const errorMessage = emailInfo.invalidEmails.length > 0 ? _t('Invalid Email') : _t("You cannot invite more than 10 people");
                this._showErrorMsg(errorMessage);
                return;
            } else {
                this._hideErrorMsg();
            }
        }
        if (appointmentForm.reportValidity()) {
            appointmentForm.submit();
            dom.addButtonLoadingEffect(event.target);
        }
    },

    /**
     * This function will hide the guest email textarea if allow_guests option is enabled.
     */
    _onHideGuest: function() {
        this._hideErrorMsg();
        const textArea = this.el.querySelector('#o_appointment_input_guest_emails');
        textArea.classList.add('d-none')
        textArea.value = "";
        const addGuestDiv = this.el.querySelector('div.o_appointment_add_guests')
        addGuestDiv.querySelector('button.o_appointment_input_guest_add').classList.remove('d-none');
        addGuestDiv.querySelector('button.o_appointment_input_guest_cancel').classList.add('d-none');
    },

    _hideErrorMsg: function() {
        const errorMsgDiv = this.el.querySelector('.o_appointment_validation_error');
        errorMsgDiv.classList.add('d-none');
    },

    _showErrorMsg: function(errorMessage) {
        const errorMsgDiv = this.el.querySelector('.o_appointment_validation_error');
        errorMsgDiv.classList.remove('d-none');
        errorMsgDiv.querySelector('.o_appointment_error_text').textContent = errorMessage;
    },

    _validateCheckboxes: function() {
        this.$el.find('.checkbox-group.required').each(function() {
            var checkboxes = $(this).find('.checkbox input');
            checkboxes.prop("required", ![...checkboxes].some((checkbox) => checkbox.checked));
        });
    },
});
