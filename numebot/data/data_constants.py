from dataclasses import dataclass


@dataclass
class NumeraiColumns:
    # Dataframe column-related names
    target: str = 'target'
    prediction: str = 'prediction'
    data_type: str = 'data_type'
    era: str = 'era'

    # Dataframe specific values
    val: str = 'validation'
    test: str = 'test'
    live: str = 'live'

    # models_configs.csv columns
    name: str = 'numerai_name'
    model_code: str = 'model_code'
    parameters: str = 'parameters'
    description: str = 'description'

    # Model round details
    model_name: str = 'username'
    round: str = 'round'
    date: str = 'date'
    correlation: str = 'correlation'

    # Model status 
    concordance: str = 'concordance'
    consistency: str = 'consistency'
    corrWithExamplePreds: str = 'corrWithExamplePreds'
    filename: str = 'filename'
    valCorrPlusMmcSharpe: str = 'validationCorrPlusMmcSharpe'
    valCorrPlusMmcSharpeDiff: str = 'validationCorrPlusMmcSharpeDiff'
    valCorrPlusMmcSharpeDiffRating: str = 'validationCorrPlusMmcSharpeDiffRating'
    valCorrPlusMmcSharpeRating: str = 'validationCorrPlusMmcSharpeRating'
    valCorrelation: str = 'validationCorrelation'
    valCorrelationRating: str = 'validationCorrelationRating'
    valFeatureExposure: str = 'validationFeatureExposure'
    valFeatureNeutralMean: str = 'validationFeatureNeutralMean'
    valFeatureNeutralMeanRating: str = 'validationFeatureNeutralMeanRating'
    valMaxDrawdown: str = 'validationMaxDrawdown'
    valMaxDrawdownRating: str = 'validationMaxDrawdownRating'
    valMaxFeatureExposure: str = 'validationMaxFeatureExposure'
    valMaxFeatureExposureRating: str = 'validationMaxFeatureExposureRating'
    valMmcMean: str = 'validationMmcMean'
    valMmcMeanRating: str = 'validationMmcMeanRating'
    valSharpe: str = 'validationSharpe'
    valSharpeRating: str = 'validationSharpeRating'
    valStd: str = 'validationStd'
    valStdRating: str = 'validationStdRating'

    # Model leaderboard
    averageCorrelationPayout = 'averageCorrelationPayout'
    badges = 'badges'
    bonusPerc = 'bonusPerc'
    leaderboardBonus = 'leaderboardBonus'
    nmrStaked = 'nmrStaked'
    oldStakeValue = 'oldStakeValue'
    payoutPending = 'payoutPending'
    payoutSettled = 'payoutSettled'
    prevRank = 'prevRank'
    prevStakedRank = 'prevStakedRank'
    rank = 'rank'
    reputation = 'reputation'
    rolling_score_rep = 'rolling_score_rep'
    stakedRank = 'stakedRank'
    tier = 'tier'
    username = 'username'

    # Others
    timestamp = 'timestamp'
    round = 'round'

NC = NumeraiColumns()
