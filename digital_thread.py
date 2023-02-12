import numpy as np
from datetime import datetime
class DigitalThread:
    def __init__(s): s.records = []; s.alerts = []
    def add(s, record):
        s.records.append({{**record, "timestamp": datetime.now().isoformat()}})
        s._check_alerts(record)
    def _check_alerts(s, record):
        for metric, threshold in {'design_complete': 100, 'mfg_quality': 98, 'delivery_otd': 95}.items():
            val = record.get(metric, None)
            if val is not None:
                if metric in {'design_complete', 'delivery_otd', 'mfg_quality'}:
                    if val < threshold: s.alerts.append({{"metric": metric, "value": val, "threshold": threshold, "severity": "critical" if val < threshold*0.85 else "warning"}})
                else:
                    if val > threshold: s.alerts.append({{"metric": metric, "value": val, "threshold": threshold, "severity": "critical" if val > threshold*1.2 else "warning"}})
    def summary(s):
        if not s.records: return {{"count": 0}}
        vals = {{}}
        for r in s.records:
            for k, v in r.items():
                if isinstance(v, (int, float)): vals.setdefault(k, []).append(v)
        stats = {{k: {{"mean": round(np.mean(v),2), "min": round(min(v),2), "max": round(max(v),2)}} for k,v in vals.items()}}
        return {{"count": len(s.records), "alerts": len(s.alerts), "critical": sum(1 for a in s.alerts if a["severity"]=="critical"), "stats": stats}}
if __name__=="__main__":
    t = DigitalThread()
    for i in range(20):
        t.add({"design_complete": np.random.normal(95, 5), "mfg_quality": np.random.normal(97, 2), "delivery_otd": np.random.normal(93, 4)})
    print(t.summary())
    for a in t.alerts[:3]: print(a)
