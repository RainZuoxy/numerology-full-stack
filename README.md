## Brief

测算八字的python库

## Sample

- **生成八字具体信息:**

```
    generate-bazi-results --name <姓名> \
    --dob-time <阳历出生时间: "%Y-%m-%d %H:%M:%S"> \
    --gender <性别: male,female> \
    --format <table:表格格式, json:json格式>
```

- **查询八卦图信息:**

```
  query-trigram --trigram-series <64卦从初爻到上爻的顺序(0为阴,1为阳)> --format <table:表格格式, json:json格式>
```
