# data pre-processing
- bmi cutoff: remove users with bmi <= 18.5
- discard users if target_weight >= weight
- discard users if hasWeightTarget = 0

# feature selection
- height：the original value

- weight：the original value

- BMI index：the original value

- average comment, post and mention

- gender: one hot encoding
- target_weight：the original value

- age：userprofile
    
    > 0：15 - 24 1：25 - 34 2：35 - 44 3：>= 45 
    >
    > use one hot encoding to 
    
- lastdays

    > combine lastdays with initial weight and target weight to define 'goal difficulty'

- weight record

    > use 4 dimension record #interval, timespan, #record, record density to define

- order record 

    > not going to use

# classification labels

- 0，1 label

  > last_weight - target_weight / target_weight > 0.25, True=1，False=0