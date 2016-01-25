# -*- coding: utf-8 -*-

from openerp import models, api
import csv
import logging

_logger = logging.getLogger(__name__)


class DataConnector(models.Model):
    _inherit = 'elvenstudio.data.connector'

    @api.model
    def export_to_md(self, filename, domain):
        status = False
        operation = self.create_operation('export_to_csv')
        operation.execute_operation('product.template')

        try:
            domain = eval(domain) if domain != '' else []
        except SyntaxError as e:
            operation.error_on_operation(e.message)

        m = self.env['product.template']
        products_to_export = m.search(domain)
        if products_to_export.ids:
            with open(filename, 'w+') as csvFile:
                writer = csv.writer(csvFile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for product in products_to_export:
                    if product.attribute_set_id:
                        pfu = 0.0
                        ic = ''
                        cv = ''
                        aderenza = ''
                        resistenza = ''
                        rumore = ''
                        battistrada = ''
                        if product.magento_attribute_ids:
                            for attribute in product.magento_attribute_ids:
                                if 'pfu' == attribute.code:
                                    pfu = attribute.value.split(' - ')[1]
                                elif 'ic_cv_singola' == attribute.code:
                                    ic = attribute.value[:-1]
                                    cv = attribute.value[-1:]
                                elif 'aderenza' == attribute.code:
                                    aderenza = attribute.value
                                elif 'resistenza' == attribute.code:
                                    resistenza = attribute.value
                                elif 'rumorosita' in attribute.code:
                                    rumore = str(attribute.value) + 'dB'
                                elif 'battistrada' == attribute.code:
                                    battistrada = attribute.value
                        '''
                        price = 0.0
                        for pricelist in product.pricelist_ids:
                            if "Listino Gommisti (Standard)" == pricelist.name:
                                price = pricelist.price
                        '''

                        # Fix a crudo per i pfu 2016
                        if pfu == '2.15':
                            pfu = '2.30'
                        elif pfu == '0.35':
                            pfu = '0.38'
                        elif pfu == '1.05':
                            pfu = '1.10'
                        elif pfu == '41.60':
                            pfu = '43.00'
                        elif pfu == '113.00':
                            pfu = '116.70'
                        elif pfu == '16.90':
                            pfu = '17.60'
                        elif pfu == '51.60':
                            pfu = '53.40'
                        elif pfu == '182.00':
                            pfu = '188.70'
                        elif pfu == '14.15':
                            pfu = '14.70'
                        elif pfu == '34.80':
                            pfu = '36.00'
                        elif pfu == '7.30':
                            pfu = '7.60'
                        elif pfu == '7.80':
                            pfu = '8.10'
                        elif pfu == '68.00':
                            pfu = '70.30'
                        elif pfu == '21.90':
                            pfu = '22.80'
                        elif pfu == '3.30':
                            pfu = '3.40'

                        price = product.with_context(pricelist=3).price
                        ip_code = product.default_code
                        if product.ip_code:
                            ip_code = product.ip_code
                        else:
                            default_code = product.default_code.split('-') if product.default_code else []
                            ip_code = default_code[1] if len(default_code) >= 2 else ''

                        imponibile = (price + float(pfu))
                        prezzo_ivato = imponibile + imponibile * 0.22

                        row = [
                            3,
                            ip_code,
                            product.compact_measure.replace('/', '') if product.compact_measure else '',
                            product.measure,
                            ic,  # IC
                            cv,  # CV
                            'XL' if product.reinforced else '',
                            'RFT' if product.runflat else '',
                            product.magento_manufacturer,
                            battistrada,
                            'SUMMER' if product.season == 'Estiva' else (
                                'WINTER' if product.season == 'Invernale' else (
                                    'ALL SEASON' if product.season == 'Quattrostagioni' else '')),
                            'CAR' if product.attribute_set_id.name == 'Pneumatico Auto' else (
                                'MOTO' if product.attribute_set_id.name == 'Pneumatico Moto' else (
                                    'AUTOCARRO' if product.attribute_set_id.name == 'Pneumatico Autocaro' else '')),
                            price if price else '0.0',
                            pfu,
                            prezzo_ivato,  # vendita + pfu + iva
                            product.qty_available,
                            product.qty_available,
                            '',  # TODO Data prox arrivo
                            product.ean13 if product.ean13 else '',
                            '',  # TODO DOT NON USATO
                            aderenza,
                            resistenza,
                            rumore,
                            ''  # TODO NETTO NON USATO
                        ]
                        writer.writerow(row)

                csvFile.close()
                status = True
                operation.complete_operation()
        else:
            operation.cancel_operation('No product selected to export')

        return status
