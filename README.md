# covid19-forecast-hub-evaluation-summary-hqj

Here I present an improved version of [YouYang Gu's evaluation](https://github.com/youyanggu/covid19-forecast-hub-evaluation) of models from the [COVID-19 Forecast Hub](https://github.com/reichlab/covid19-forecast-hub).

The evaluation consists of two steps.
1. **Evaluation** level - Every week, the percentage error of a model is calculated. Models are ranked based on 1-6w performance. (This step is exactly the same and copied from YYG's evaluation)
2. **Summary** level - I calculate median/mean/std of historical weekly ranking, as well as RMSE/MAE of historical weekly 1-6w error. Models are ranked based on these two metrics.

Each model has the option to exclude the three earliest submissions, as it takes time to build a robust and reliable model.

**Differences and what is improved**
1. Step 2 gives **direct** and **primary** data of historical weekly ranking and error. In contrast, YYG's summary gives **indirect** data - it involves an additional layer of "beating the baseline". This does not reflect the true performance of a model. For exmaple, we compare a good model (error 5%) and a poor model (error 50%). When baseline error is 70%, each model scores 1 point. When baseline error is 1%, each model scores 0 point. Under these circumstances, YYG's approach cannot distinguish the models.
2. Models are ranked based on their 1-4 week forward projection. Many models do not provide forecast beyond 4 weeks, so YYG's evaluation is unfair to these models. 

Sorted by median of weekly ranking
![Sorted by median of weekly ranking](https://github.com/qjhong/covid19-forecast-hub-evaluation-summary-hqj/blob/main/Rank_Summary.png)
Sorted by mean of 1234w RMSE
![Sorted by mean of 1234w RMSE](https://github.com/qjhong/covid19-forecast-hub-evaluation-summary-hqj/blob/main/Rank_RMSE_Summary.png)
