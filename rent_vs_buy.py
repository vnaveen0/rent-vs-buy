import numpy_financial as npf

def monthly_cost(total_years, downpayment_rate, closing_cost_rate, orig_house_cost, interest_rate):

    # Buy House Constants
    property_tax_rate = 0.29/100.0
    # Maint. + strata etc
    maintenance_rate = 1/100.0 
    # utilities = 200.0
    house_appreciation_rate = 6/100.0

    # Renting Constants
    orig_rent = 3000
    rent_increase_rate = 2/100.0
    investment_return_rate = 10/100.0

    print("=============")
    print("Buy House")
    print("=============")


    total_installments = total_years*12
    monthly_interest_rate = interest_rate/12
    monthly_house_appreciation = house_appreciation_rate/12
    
    # One time cost
    closing_cost = closing_cost_rate*orig_house_cost
    closing_cost_monthly = closing_cost/total_years/12

    # Monthly Recurring Costs 
    loan_amount = orig_house_cost* (1 - downpayment_rate)
    emi_monthly = -1*npf.pmt(monthly_interest_rate,total_installments,loan_amount)
    #Utilities is higher in buying
  
    # If I invest the downpayment + closing cost amount
    total_installments = total_years*12
    orig_investment = orig_house_cost*downpayment_rate + closing_cost_rate*orig_house_cost
    # print("Original Investment: {}".format(orig_investment))
    future_asset_value = round(-1*npf.fv(investment_return_rate/12.0,total_installments,0,orig_investment))
    
    # Every Year Cost 
    total_cost_when_buying = 0
    total_rent = 0
    total_diff_invested = 0
    for i in range(0, total_years):
        current_house_value = -1*npf.fv(house_appreciation_rate,i,0,orig_house_cost)
        maintenance_monthly = maintenance_rate*current_house_value/12
        property_tax_monthly = property_tax_rate*current_house_value/12
        
        total_cost_when_buying_monthly = emi_monthly + maintenance_monthly + property_tax_monthly + closing_cost_monthly
        total_cost_when_buying_yearly = total_cost_when_buying_monthly*12
        # print("Year: {} Total Yr Cost: {} emi: {}, maint: {}, property_tax: {} closing: {}".format(i, total_cost_when_buying_yearly, 
        #                                                                             emi_monthly, 
        #                                                                             maintenance_monthly, 
        #                                                                             property_tax_monthly, closing_cost_monthly)) 
        total_cost_when_buying += total_cost_when_buying_yearly


        

        current_value_of_orig_investment = round(-1*npf.fv(investment_return_rate/12.0,i*12,0,orig_investment))
        diff_amount_investment = 0
        if i ==0:
            current_rent = orig_rent
            diff_amount = emi_monthly - current_rent
            if diff_amount>0:
                diff_amount_investment = diff_amount
            else:
                diff_amount_investment = 0
            
        else:
            current_rent = orig_rent*pow((1 + rent_increase_rate),i)
            diff_amount = current_rent - emi_monthly
            if diff_amount>0:
                diff_amount_investment = total_diff_invested*pow((1 + investment_return_rate),i) + diff_amount
            else:
                diff_amount_investment = total_diff_invested*pow((1 + investment_return_rate),i)
        
        # print("YR: {}, Diff: {} ")
        total_diff_invested += diff_amount_investment
        current_invest_value = round(current_value_of_orig_investment + total_diff_invested)

        total_rent +=current_rent 

        diff_rent_minus_buy = round(current_rent*12 - total_cost_when_buying_yearly)
        print("Year: {} Yrly Cost/Renting {} Yrly Cost/Buying {}. Yrly Diff: {}. Current Invest.Value:{} Current House Value: {}".
              format(i, round(total_rent), round(total_cost_when_buying_yearly), diff_rent_minus_buy, 
                     current_invest_value, round(current_house_value))) 
    
    print("Total Paid: {}".format(round(total_cost_when_buying)))
    # Future house Value
    future_house_cost = round(-1*npf.fv(monthly_house_appreciation,total_installments,0,orig_house_cost))
    print("Future House Value: {}".format(future_house_cost))
    buy_profit = round(future_house_cost - total_cost_when_buying)
    print("Diff: {}".format(buy_profit))


    print("=============")
    print("Rent House")
    print("=============")

    print("Total Rent: {}".format(total_rent))



    
    # If I invest the difference in rent as well

    
    
    print("Future Asset Value: {}".format(future_asset_value))
    rent_profit = round(future_asset_value - total_rent)
    print("Diff: {}".format(rent_profit))


    print("=============")
    diff = round(buy_profit - rent_profit)
    print("Buy - Rent = {}".format(diff))

if __name__ == "__main__":
    
    total_years = 30
    orig_house_cost = 700000
    downpayment_rate = 10/100.0
    closing_cost_rate = 1.5/100.0
    interest_rate = 4/100.0
    closing_cost = closing_cost_rate*orig_house_cost


    monthly_cost(total_years, downpayment_rate, closing_cost_rate, orig_house_cost, interest_rate)
