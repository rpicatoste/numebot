import matplotlib.pyplot as plt
import pandas as pd


def plot_time_metrics(performances, my_usernames):

    _=plt.figure(figsize=(10,8))
    ax_1 = plt.subplot(4,1,1)
    ax_2 = plt.subplot(4,1,2, sharex=ax_1)
    ax_3 = plt.subplot(4,1,3, sharex=ax_2)
    ax_4 = plt.subplot(4,1,4, sharex=ax_3)

    ax_1_name = 'normalized_payout'
    ax_2_name = 'normalized_payout cumsum'
    ax_3_name = 'corr'
    ax_4_name = 'tc'

    for model_slot_name in my_usernames:
        df = performances[model_slot_name].copy().sort_values('roundOpenTime').reset_index(drop=True)
        empty_filter = df['corr'].isna()
        df = df[~empty_filter]

        # Remove non-staked models
        if df['selectedStakeValue'].sum() < 1:
            continue

        at_risk_stake = 100.0
        corr_part = df['corr'] * df['corrMultiplier']
        tc_part = df['tc'] * df['mmcMultiplier']
        df['normalized_payout'] = at_risk_stake * (df['roundPayoutFactor'].astype(float) * (corr_part + tc_part)).clip(lower=-0.25, upper=0.25)

        col = ax_1_name
        _=ax_1.plot(df['roundOpenTime'], df[col], '-o', label=model_slot_name)

        rounds_cums = '2022-08-01'
        filter_rounds = df['roundOpenTime'] > rounds_cums
        _=ax_2.plot(df.loc[filter_rounds, 'roundOpenTime'], df.loc[filter_rounds, col].cumsum(), '-o', label=model_slot_name)

        col = ax_3_name
        _=ax_3.plot(df['roundOpenTime'], df[col], '-o', label=model_slot_name)

        col = ax_4_name
        _=ax_4.plot(df['roundOpenTime'], df[col], '-o', label=model_slot_name)

    _=ax_1.set_title(ax_1_name)
    _=ax_2.set_title(ax_2_name)
    _=ax_3.set_title(ax_3_name)
    _=ax_4.set_title(ax_4_name)

    _=ax_1.set_ylabel(ax_1_name)
    _=ax_2.set_ylabel(ax_2_name)
    _=ax_3.set_ylabel(ax_3_name)
    _=ax_4.set_ylabel(ax_4_name)

    _=ax_1.grid()
    _=ax_2.grid()
    _=ax_3.grid()
    _=ax_4.legend(), ax_4.grid()


def plot_aggregated_metrics(performances, my_usernames, period_in_months=None):

    _=plt.figure(figsize=(10,8))
    ax_1 = plt.subplot(4,2,1)
    ax_2 = plt.subplot(4,2,3, sharex=ax_1)
    ax_3 = plt.subplot(4,2,5, sharex=ax_2)

    ax_1_name = 'normalized_payout'
    ax_2_name = 'corr'
    ax_3_name = 'tc'

    # Get date from start of period
    if period_in_months is not None:
        start_date = pd.to_datetime('today') - pd.DateOffset(months=period_in_months)
    else:
        # Take the fist roundOpenTime
        start_date = performances[my_usernames[0]]['roundOpenTime'].min()

    for model_slot_name in my_usernames:
        df = performances[model_slot_name].copy().sort_values('roundOpenTime').reset_index(drop=True)
        empty_filter = df['corr'].isna()
        df = df[~empty_filter]

        # Filter by period
        filter_rounds = df['roundOpenTime'] > str(start_date.date())
        
        df = df[filter_rounds]

        # Remove non-staked models
        if df['selectedStakeValue'].sum() < 1:
            continue

        at_risk_stake = 100.0
        corr_part = df['corr'] * df['corrMultiplier']
        tc_part = df['tc'] * df['mmcMultiplier']
        df['normalized_payout'] = at_risk_stake * (df['roundPayoutFactor'].astype(float) * (corr_part + tc_part)).clip(lower=-0.25, upper=0.25)

        col = ax_1_name
        _=ax_1.plot(df['roundOpenTime'].count(), df[col].mean(), '-o', label=model_slot_name)

        #_=ax_2.plot(df.loc[filter_rounds, 'roundOpenTime'].count(), df.loc[filter_rounds, col].cumsum(), '-o', label=model_slot_name)

        col = ax_2_name
        _=ax_2.plot(df['roundOpenTime'].count(), df[col].mean(), '-o', label=model_slot_name)

        col = ax_3_name
        _=ax_3.plot(df['roundOpenTime'].count(), df[col].mean(), '-o', label=model_slot_name)

    _=ax_1.set_title(ax_1_name)
    _=ax_2.set_title(ax_2_name)
    _=ax_3.set_title(ax_3_name)

    if period_in_months is not None:
        _=ax_1.set_title(ax_1_name + f' (last {period_in_months} months)')
        _=ax_2.set_title(ax_2_name + f' (last {period_in_months} months)')
        _=ax_3.set_title(ax_3_name + f' (last {period_in_months} months)')

    _=ax_1.set_ylabel(ax_1_name)
    _=ax_2.set_ylabel(ax_2_name)
    _=ax_3.set_ylabel(ax_3_name)

    _=ax_1.grid()
    _=ax_2.grid()
    _=ax_3.legend(), ax_3.grid()

    # Now plot the stake

    ax_1 = plt.subplot(4,2,2)
    ax_2 = plt.subplot(4,2,4, sharex=ax_1)
    ax_3 = plt.subplot(4,2,6, sharex=ax_2)

    ax_1_name = 'selectedStakeValue'
    ax_2_name = 'corr'
    ax_3_name = 'tc'

    # Get date from start of period
    if period_in_months is not None:
        start_date = pd.to_datetime('today') - pd.DateOffset(months=period_in_months)
    else:
        # Take the fist roundOpenTime
        start_date = performances[my_usernames[0]]['roundOpenTime'].min()

    for model_slot_name in my_usernames:
        df = performances[model_slot_name].copy().sort_values('roundOpenTime').reset_index(drop=True)
        empty_filter = df['corr'].isna()
        df = df[~empty_filter]

        # Remove non-staked models
        if df['selectedStakeValue'].sum() < 1:
            continue

        # Remove nan stakes
        df = df[df['selectedStakeValue'].notna()]
        

        col = ax_1_name
        _=ax_1.plot(df['roundOpenTime'].iloc[-1], df[col].iloc[-1], '-o', label=model_slot_name)

        # col = ax_2_name
        # _=ax_2.plot(df['roundOpenTime'].count(), df[col].mean(), '-o', label=model_slot_name)

        # col = ax_3_name
        # _=ax_3.plot(df['roundOpenTime'].count(), df[col].mean(), '-o', label=model_slot_name)

    _=ax_1.set_title(ax_1_name)
    _=ax_2.set_title(ax_2_name)
    _=ax_3.set_title(ax_3_name)

    _=ax_1.set_ylabel(ax_1_name)
    _=ax_2.set_ylabel(ax_2_name)
    _=ax_3.set_ylabel(ax_3_name)

    _=ax_1.grid()
    _=ax_2.grid()
    _=ax_3.legend(), ax_3.grid()

    plt.tight_layout()