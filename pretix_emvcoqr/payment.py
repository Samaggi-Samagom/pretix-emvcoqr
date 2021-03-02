from collections import OrderedDict
from decimal import Decimal
import crc16
import qrcode
import base64
from io import BytesIO
from i18nfield.forms import I18nFormField
from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from pretix.base.payment import ManualPayment


class EMVCoQRPayment(ManualPayment):
    identifier = 'emvcoqr'
    verbose_name = _('EMVCo QR Code + Manual payment')

    def __init__(self, event):
        super().__init__(event)

    def is_implicit(self, request):
        return super(ManualPayment, self).is_implicit(request)

    def is_allowed(self, request, total=None):
        return super(ManualPayment, self).is_allowed(request, total)

    def order_change_allowed(self, order):
        return super(ManualPayment, self).order_change_allowed(order)

    @property
    def settings_form_fields(self):
        d = OrderedDict(
            [
                ('emvco_qrcode_data', forms.CharField(
                    label=_('EMVCo QR data string'),
                    help_text=_('This is the data to be encoded in the QR Code. '
                                'Please include every details you need except the payment amount and the checksum. '
                                '(Those two entries will be included automatically) '
                                'For more information on how to contruct this string, please see '
                                'https://python3.wannaphong.com/2017/09/qr-code-promptpay-python.html and '
                                'https://medium.com/@sikawit/%E0%B8%A1%E0%B8%B5%E0%B8%AD%E0%B8%B0%E0%B9%84%E0%B8%A3%E0%B8'
                                '%AD%E0%B8%A2%E0%B8%B9%E0%B9%88%E0%B9%83%E0%B8%99-qr-promptpay-services-84ed6216a267 '
                                'as well as the source code of this plugin.'),
                )),
            ] + list(super().settings_form_fields.items())
        )
        pending_description_field: I18nFormField = d['pending_description']
        pending_description_field.help_text = \
            _('This text will be shown on the order confirmation page for pending orders. '
              'It should instruct the user on how to proceed with the payment. You can use '
              'the placeholders {order}, {total}, {currency} and {total_with_currency}. '
              'Also, to include the QR Code in the description use %%QR%%.')
        # email_instructions_field: I18nFormField = d['email_instructions']
        # email_instructions_field.help_text = \
        #     _('This text will be included for the {payment_info} placeholder in order confirmation '
        #       'mails. It should instruct the user on how to proceed with the payment. You can use '
        #       'the placeholders {order}, {total}, {currency} and {total_with_currency}. '
        #       'Also, to include the QR Code in the instructions use %%QR%%.')
        d.move_to_end('_enabled', last=False)
        return d

    def generate_qr_text(self, amount: Decimal) -> str:
        # If the amount has less than two floating points, increase the floating points to two
        if amount.as_tuple().exponent > -2:
            amount = amount.quantize(Decimal('1.23'))
        amount_str = str(amount)
        money_str = '54{:02d}{}'.format(len(amount_str), amount_str)

        # Original credit for this: https://github.com/wannaphong/pypromptpay/blob/master/pypromptpay.py#L47
        before_check_sum = self.settings.get('emvco_qrcode_data', '0002' + '01') + money_str + '6304'
        check_sum = hex(crc16.crc16xmodem(before_check_sum.encode("ascii"), 0xffff)).replace('0x', '')
        if len(check_sum) < 4:  # Increase the checksum length to 4
            check_sum = ("0" * (4 - len(check_sum))) + check_sum

        qr_text = before_check_sum + check_sum
        return qr_text.upper()

    def generate_qr_image(self, qr_text):
        image = qrcode.make(qr_text)
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()

    def payment_pending_render(self, request, payment) -> str:
        html = super().payment_pending_render(request, payment)
        # payment.amount definition:
        # https://github.com/pretix/pretix/blob/be67059099b73d6f01217968eba0f041026331e8/src/pretix/base/models/orders.py#L1333
        img_tag = '<img src="data:image/png;base64,{}" width="250" height="250" />' \
            .format(self.generate_qr_image(self.generate_qr_text(payment.amount)))
        return mark_safe(html.replace('%%QR%%', img_tag))

# Image is not allowed in pretix email
#    def order_pending_mail_render(self, order) -> str:
#        html = super().order_pending_mail_render(order)
#        img_tag = '<img src="data:image/png;base64,{}" width="50" height="50" />' \
#            .format(self.generate_qr_image(self.generate_qr_text(order)))
#        return mark_safe(html.replace('%%QR%%', img_tag))
