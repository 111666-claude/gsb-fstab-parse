# fstab-parse

解析 /etc/fstab：字段切分、选项映射、同挂载点覆盖、按路径深度与 pass 排挂载顺序。只用 Python 标准库。

```
python3 -m unittest discover -s tests
python3 -m fstab --sample=options
python3 -m fstab --sample=overlay
python3 -m fstab --sample=order
python3 -m fstab --sample=pass
python3 -m fstab --sample=work
```

## 口径

- **字段**：设备、挂载点、文件系统类型、选项、dump、pass；`#` 到行尾是注释。
- **选项**：逗号分隔；`k=v` 记成键值对，单独的记成值为空串的键。
- **覆盖**：同一个挂载点出现多次时后者覆盖前者。
- **顺序**：先挂父目录再挂子目录；同层按 pass 升序，再按出现顺序。
- **查找**：按挂载点查找走索引。

## 不变量

- 每个挂载点在解析结果里只有一条。
- 挂载顺序里父路径一定排在子路径之前。
- `scanned` 不随条目数乘查询次数放大：八百条查八百次的 `scanned` 不超过 6000。

## 输出契约

`Entry` 含设备、挂载点、类型、选项映射、dump 与 pass。场景打印一行 JSON。
`--sample=work` 打印 `{"entries": N, "scanned": N}`。
