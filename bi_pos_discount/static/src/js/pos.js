/** @odoo-module */

import { PosStore } from "@point_of_sale/app/store/pos_store";
import { Order,Orderline } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";
import { roundPrecision as round_pr, floatIsZero } from "@web/core/utils/numbers";
import { parseFloat as oParseFloat } from "@web/views/fields/parsers";

patch(PosStore.prototype, {
    // @Override
    async _processData(loadedData) {
        await super._processData(...arguments);
        this.pos_order = loadedData['pos_order'] || [];
       
    },
   
});

patch(Order.prototype, {
	init_from_JSON(json){
		super.init_from_JSON(...arguments);
//		this.discount_type = json.discount_type;
		this.discount_type = this.pos.config.discount_type;
	},
	export_as_JSON(){
		const json = super.export_as_JSON(...arguments);
		json.discount_type = this.discount_type || false;
		json.discount_type = this.pos.config.discount_type || false;
		return json;
	},
	set_orderline_options(orderline,options){
		super.set_orderline_options(...arguments);
		if(options.discount_type){
        	orderline.discount_type = options.discount_type
//        	this.discount_type = options.discount_type
        	this.discount_type = this.pos.config.discount_type
        }
	},
	get_fixed_discount(){
		var total=0.0;
		var i;
		var orderlines = this.get_orderlines()
		for(i=0;i<orderlines.length;i++) 
		{	
			total = total + parseFloat(orderlines[i].discount);
		}
		return total
	},

	get_total_discount(){
		var self = this;
        return round_pr(this.orderlines.reduce((function(sum, orderLine) {
        	if(orderLine.discount_type){
        		if (orderLine.discount_type == "Percentage"){
	        		sum += parseFloat(orderLine.get_unit_price() * (orderLine.get_discount()/100) * orderLine.get_quantity());
		            if (orderLine.display_discount_policy() === 'without_discount'){
		                sum += parseFloat(((orderLine.get_lst_price() - orderLine.get_unit_price()) * orderLine.get_quantity()));
		            }
		            return sum;
	        	}
	        	else{
	        		sum += parseFloat(orderLine.get_discount());
		            if (orderLine.display_discount_policy() === 'without_discount'){
		                sum += parseFloat(((orderLine.get_lst_price() - orderLine.get_unit_price()) * orderLine.get_quantity()));
		            }
		            return sum;
	        	}
        	}
        	else{
        		if (self.pos.config.discount_type == 'percentage'){
	        		sum += parseFloat(orderLine.get_unit_price() * (orderLine.get_discount()/100) * orderLine.get_quantity());
		            if (orderLine.display_discount_policy() === 'without_discount'){
		                sum += parseFloat(((orderLine.get_lst_price() - orderLine.get_unit_price()) * orderLine.get_quantity()));
		            }
		            return sum;
	        	}
	        	if(self.pos.config.discount_type == 'fixed'){
	        		sum += parseFloat(orderLine.get_discount());
		            if (orderLine.display_discount_policy() === 'without_discount'){
		                sum += parseFloat(((orderLine.get_lst_price() - orderLine.get_unit_price()) * orderLine.get_quantity()));
		            }
		            return sum;
	        	}
        	}
        }), 0), this.pos.currency.rounding);
	}
    
});


patch(Orderline.prototype, {
	init_from_JSON(json){
		super.init_from_JSON(...arguments);
//		this.discount_type = json.discount_type;
		this.discount_type = this.pos.config.discount_type;
	},
	export_as_JSON(){
		const json = super.export_as_JSON(...arguments);
//		json.discount_type = this.discount_type || false;
		json.discount_type = this.pos.config.discount_type || false;
		return json;
	},
	set_discount(discount){

		var parsed_discount =
            typeof discount === "number"
                ? discount
                : isNaN(parseFloat(discount))
                ? 0
                : oParseFloat("" + discount);
		// var parsed_discount = typeof(discount) === 'number' ? discount : isNaN(parseFloat(discount)) ? 0 : field_utils.parse.float('' + discount);
		if (parsed_discount < 0) {
		    this.discount = 0;
		} else {
            if (this.refunded_orderline_id){
                if(this.discount){
                    if (this.discount_type == 'Percentage'){
                        var disc = Math.min(Math.max(parseFloat(parsed_discount) || 0, 0),100);
                    }
                    if (this.discount_type == 'Fixed'){
                        var disc = parsed_discount || 0;
                    }
                }

            }
            else{
        		
                if (this.pos.config.discount_type == 'percentage'){
                    var disc = Math.min(Math.max(parseFloat(parsed_discount) || 0, 0),100);
                }
                if (this.pos.config.discount_type == 'fixed'){
                    var disc = parsed_discount || 0;
                }
            }
            this.discount = disc;
            this.discountStr = '' + disc;
        }
	},
	get_base_price(){
		var rounding = this.pos.currency.rounding;
		if(this.discount_type){
			if (this.discount_type == 'Percentage')
			{
				return round_pr(this.get_unit_price() * this.get_quantity() * (1 - this.get_discount()/100), rounding);
			}
			if (this.discount_type == 'Fixed')
			{
				return round_pr((this.get_unit_price()* this.get_quantity())-(this.get_discount()), rounding);	
			}
		}else{
			if (this.pos.config.discount_type == 'percentage')
			{
				return round_pr(this.get_unit_price() * this.get_quantity() * (1 - this.get_discount()/100), rounding);
			}
			if (this.pos.config.discount_type == 'fixed')
			{
				return round_pr((this.get_unit_price()* this.get_quantity())-(this.get_discount()), rounding);	
			}
		}
	},
	get_all_prices(){
		if(this.discount_type){
			if (this.discount_type == 'Percentage')
			{
				var price_unit = this.get_unit_price() * (1.0 - (this.get_discount() / 100.0));
			}
			if (this.discount_type == 'Fixed')
			{
				// var price_unit = this.get_unit_price() - this.get_discount();
				var price_unit = this.get_base_price()/this.get_quantity();		
			}
		}else{
			if (this.pos.config.discount_type == 'percentage')
			{
				var price_unit = this.get_unit_price() * (1.0 - (this.get_discount() / 100.0));
			}
			if (this.pos.config.discount_type == 'fixed')
			{
				// var price_unit = this.get_unit_price() - this.get_discount();
				var price_unit = this.get_base_price()/this.get_quantity();		
			}
		}	
		var taxtotal = 0;

		var product =  this.get_product();
		var taxes_ids = product.taxes_id;
		var taxes =  this.pos.taxes;
		var taxdetail = {};
		var product_taxes = this.pos.get_taxes_after_fp(taxes_ids, this.order.fiscal_position);

		var all_taxes = this.compute_all(product_taxes, price_unit, this.get_quantity(), this.pos.currency.rounding);
		var all_taxes_before_discount = this.compute_all(product_taxes, this.get_unit_price(), this.get_quantity(), this.pos.currency.rounding);
		all_taxes.taxes.forEach(function (tax) {
            taxtotal += tax.amount;
            taxdetail[tax.id] = {
                amount: tax.amount,
                base: tax.base,
            };
        });
		return {
			"priceWithTax": all_taxes.total_included,
            "priceWithoutTax": all_taxes.total_excluded,
            "priceSumTaxVoid": all_taxes.total_void,
            "priceWithTaxBeforeDiscount": all_taxes_before_discount.total_included,
            "tax": taxtotal,
            "taxDetails": taxdetail,
		};

	},

	get_orderline_discount_type(){
		return this.pos.config.discount_type;
	},

	getDisplayData() {
		return {
			productName: this.get_full_product_name(),
			price: this.env.utils.formatCurrency(this.get_display_price()),
			qty: this.get_quantity_str(),
			unit: this.get_unit().name,
			unitPrice: this.env.utils.formatCurrency(this.get_unit_display_price()),
			oldUnitPrice: this.env.utils.formatCurrency(this.get_old_unit_display_price()),
			discount: this.get_discount_str(),
			customerNote: this.get_customer_note(),
			internalNote: this.getNote(),
			comboParent: this.comboParent?.get_full_product_name(),
			discount_type : this.get_orderline_discount_type(),
			line_discount_type : this.pos.config.discount_type,
		};
	},
	get_display_price_one(){
		var rounding = this.pos.currency.rounding;
		var price_unit = this.get_unit_price();
		if (this.pos.config.iface_tax_included !== 'total') {

			if(this.discount_type){
				if (this.discount_type == 'Percentage')
				{
					return round_pr(price_unit * (1.0 - (this.get_discount() / 100.0)), rounding);
				}
				if (this.discount_type == 'Fixed')
				{
					return round_pr(price_unit  - (this.get_discount()/this.get_quantity()), rounding);
				}
			}
			else{

				if (this.pos.config.discount_type == 'percentage')
				{
					return round_pr(price_unit * (1.0 - (this.get_discount() / 100.0)), rounding);
				}
				if (this.pos.config.discount_type == 'fixed')
				{
					return round_pr(price_unit  - (this.get_discount()/this.get_quantity()), rounding);
				}
			}	

		} else {
			var product =  this.get_product();
			var taxes_ids = product.taxes_id;
			var taxes =  this.pos.taxes;
			var product_taxes = [];

			_(taxes_ids).each(function(el){
				product_taxes.push(_.detect(taxes, function(t){
					return t.id === el;
				}));
			});

			var all_taxes = this.compute_all(product_taxes, price_unit, 1, this.pos.currency.rounding);
			if (this.discount_type){
				if (this.discount_type == 'Percentage')
				{
					return round_pr(all_taxes.total_included * (1 - this.get_discount()/100), rounding);
				}
				if (this.discount_type == 'Fixed')
				{
					return round_pr(all_taxes.total_included  - (this.get_discount()/this.get_quantity()), rounding);
				}
			}else{
				if (this.pos.config.discount_type == 'percentage')
				{
					return round_pr(all_taxes.total_included * (1 - this.get_discount()/100), rounding);
				}
				if (this.pos.config.discount_type == 'fixed')
				{
					return round_pr(all_taxes.total_included  - (this.get_discount()/this.get_quantity()), rounding);
				}
			}	
		}
	}
    
});

