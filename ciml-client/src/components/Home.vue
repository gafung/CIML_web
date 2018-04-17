<template>
    <el-container>
        <el-header>
            Homepage {{ msg }}
        </el-header>
        <el-main>
            <div>Main</div>
            <div>a</div>
        </el-main>
    </el-container>
</template>
<script>

export default {
    name: 'Home',
    data() {
        return {
            msg: 'YAY',
        };
    }
}
</script>