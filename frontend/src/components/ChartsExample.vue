<script>
export default {
  name: "ChartsExample"
}
</script>

<template>
<div class="example-section">
        <h2>
          <img src="../assets/images/table-icon.svg" alt="表格图标">
          表格示例
        </h2>
        <div class="example-table-container">
          <table class="example-table">
            <thead>
              <tr>
                <th>编号</th>
                <th>性别</th>
                <th>年龄</th>
                <th>学历</th>
                <th>年收入</th>
                <th>日期</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>1</td>
                <td>1</td>
                <td>32</td>
                <td>本科</td>
                <td>2</td>
                <td>2021/8/12</td>
              </tr>
              <tr>
                <td>2</td>
                <td>1</td>
                <td>28</td>
                <td>硕士</td>
                <td>3</td>
                <td>2021/8/13</td>
              </tr>
              <tr>
                <td>3</td>
                <td>2</td>
                <td>35</td>
                <td>本科</td>
                <td>4</td>
                <td>2021/8/14</td>
              </tr>
              <tr>
                <td>4</td>
                <td>2</td>
                <td>40</td>
                <td>博士</td>
                <td>5</td>
                <td>2021/8/15</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
</template>

<style scoped>
.example-section h2 {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 20px;
  color: #303133;
  margin-bottom: 20px;
}

.example-table-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 20px;
  overflow-x: auto;
}

.example-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.example-table th,
.example-table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #ebeef5;
}

.example-table th {
  background-color: #f5f7fa;
  font-weight: 600;
  color: #606266;
}

.example-table tbody tr:hover {
  background-color: #f5f7fa;
}

@media (max-width: 768px) {
    .example-table {
    font-size: 12px;
  }

  .example-table th,
  .example-table td {
    padding: 8px 10px;
  }
}
</style>