# cleaning process
> each step.py has more detailed description，just list some rationale of data cleaning here

- missing values: if any entry of certain users is missing，we just discard these users<br>

- filter out the rest if the filtering condition holds<br>
> - height < 100cm
> - weight < 30kg
> - lastdays < 10
> - bmi < 18.5
> - hastarget_weigt = 0 -> target_weight = 0
> - target_weight >= weight
> - gender = 0

# final user features
> id,height,weight,target_weight,bmi,man,women,AvgPost,AvgComment,AvgMention,lastdays,age,diffcult
>>
> | id         | height     | weight     | target_weight | bmi     | man          | woman |
> | --------- | ---------- | ---------- | ------------- | ------- | ------------ | ----- |
> | AvgPost    | AvgComment | AvgMention | lastdays      | age     | diffcult     |       |
>
> final users：1355905
# label assigning
>
> calculate by：$(weight - last\_record\_weight)\ /\   (weight - target\_weight) $
>
> | range             | label | users | ratio |
> | ----------------- | ---- | -------- | -------- |
> | $(-\infty, 0.25]$ | 0    | 1024561  | 0.756    |
> | $(0.25, 0.5]$     | 1    | 216167   | 0.159    |
> | $(0.5, 0.75]$     | 2    | 77287    | 0.057    |
> | $(0.75, +\infty)$ | 3    | 37890    | 0.028    |
> | total             |      | 1355905  | 1        |
>
> 

