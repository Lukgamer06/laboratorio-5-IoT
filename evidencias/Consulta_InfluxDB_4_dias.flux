from(bucket: "iot_lab5")
  |> range(start: -4d)
  |> filter(fn: (r) => r["_measurement"] == "environment")
  |> filter(fn: (r) =>
    r["_field"] == "temperature" or
    r["_field"] == "humidity" or
    r["_field"] == "illuminance"
  )
  |> aggregateWindow(every: 1m, fn: mean, createEmpty: false)
