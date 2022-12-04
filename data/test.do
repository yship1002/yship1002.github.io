cd "Z:\Documents\2022Fall\DataScience\Project\yship1002.github.io\data"
clear all
import delimited "Z:\Documents\2022Fall\DataScience\Project\yship1002.github.io\data\Small_Data.csv"
ssc install oaxaca
*drop if income==0
*xi: oaxaca approved i.married i.industry age i.ethnicity i.priordefault income i.employed i.citizen, by(gender) vce(robust) swap relax pooled
replace priordefault=-priordefault
gen credit_util=debt/income
gen is_male=1 if gender==1
replace is_male=0 if gender!=1
gen ethnicity_is_black=1 if ethnicity=="Black"
replace ethnicity_is_black=0 if ethnicity!="Black"
egen ethnicity_is_black_z=std(ethnicity_is_black)
egen is_male_z=std(is_male)
egen priordefault_z=std(priordefault)
egen income_z=std(income)
egen debt_z=std(debt)
egen age_z=std(age)
egen credit_util_z=std(credit_util)
xi: regress approved ethnicity_is_black_z income_z priordefault_z age_z is_male_z credit_util_z
xi: logit approved ethnicity_is_black_z income_z priordefault_z age_z is_male_z credit_util_z
*oaxaca approved age reports share majorcards, by(high_income) vce(robust) swap relax pooled
*xi: oaxaca approved debt age i.industry i.ethnicity i.employed income i.citizen i.priordefault i.married, by(gender) vce(robust) swap relax pooled