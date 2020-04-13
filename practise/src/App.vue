<template>
<div class="container">
  <h2>我的购物车清单</h2>
  <!-- 输入框，添加按钮 -->
  <div class="input-group">
    <input type="text" class="js-new-item form-control" placeholder="添加想要购买的商品" />
    <span class="input-group-btn">
      <button type="button" class="js-add btn btn-default">添加到购物车</button>
    </span>
  </div>

  <!-- 无序列表 -->
  <ul>
    <li>
      <div class="checkbox">
        <label for>
          <input class="js-item" type="checkbox" />苹果
        </label>
      </div>
    </li>
    <li>
      <div class="checkbox">
        <label for>
          <input class="js-item" type="checkbox" />手机
        </label>
      </div>
    </li>
    <li>
      <div class="checkbox">
        <label for>
          <input class="js-item" type="checkbox" />电脑
        </label>
      </div>
    </li>
  </ul>

  <!-- 改变标题 -->
  <div class="footer">
    <hr />
    <span>改变标题</span>
    <input type="text" value="我的购物车清单" class="js-change-title" />
  </div>
</div>
</template>

<script>
</script>

<style>
.container {
  width: 40%;
  margin: 100px auto;
}
.removed {
  color: grey;
}
.removed label {
  text-decoration: line-through;
}
ul {
  border: 1px solid black;
  margin-top: 30px;
}
ul li {
  list-style: none;
}
</style>
