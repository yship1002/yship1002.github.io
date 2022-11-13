cd "Z:\Documents\2022Fall\DataScience\Project\yship1002.github.io\data"
clear all
import delimited "Z:\Documents\2022Fall\DataScience\Project\yship1002.github.io\data\Small_Data.csv"
ssc install oaxaca
*xi: oaxaca approved i.married i.industry age i.ethnicity i.priordefault income i.employed i.citizen, by(gender) vce(robust) swap relax pooled

xi: oaxaca approved debt age i.industry i.ethnicity i.employed income i.citizen i.priordefault i.married, by(gender) vce(robust) swap relax pooled