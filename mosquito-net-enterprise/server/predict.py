def malaria_risk(rainfall, temperature, net_coverage, population):
    risk = 0.4*rainfall + 0.3*temperature - 0.5*net_coverage + 0.2*population
    return min(max(risk,0),100)
