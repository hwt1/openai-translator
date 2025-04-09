<template>
  <div id="translate-page">
    <h1>翻译页面</h1>
    <!-- 这里添加你的页面内容 -->
    <el-form :model="form" @submit.prevent="handleSubmit" style="width: 60%">

      <el-row>
        <el-col :span="12">
          <el-form-item label="选择翻译模型">
            <el-select
                v-model="form.modelName"
                class="m-2"
                size="large"
                style="width: 240px">
              <el-option
                  v-for="item in modelNames"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
              />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row style="width: 40%">
        <el-col :span="24">
          <el-form-item label="上传文件">
            <el-upload
              class="upload-demo"
              drag
              :auto-upload="false"
              accept=".pdf"
              limit="1"
              :on-change="handleFileChange"
              :on-exceed="handleExceed"
              :on-error="handleError">
              <el-icon class="el-icon--upload"><upload-filled />
              </el-icon>
            <div class="el-upload__text">
              将文件拖拽至此处 或者 <em>点击上传文件</em>
            </div>
            <template #tip>
              <div class="el-upload__tip">
                只支持上传 <strong>pdf</strong> 格式的文件，且文件大小不超过 <strong>1MB</strong>
              </div>
            </template>
          </el-upload>
          </el-form-item>
        </el-col>
      </el-row>
      <el-form-item>
        <el-button type="primary" native-type="submit">提交</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { UploadFilled } from '@element-plus/icons-vue'
export default {
  name: 'TranslatePage',
  components: {
    UploadFilled
  },
  data() {
    return {
      modelNames: [
        { value: 'gpt-3.5-turbo', label: 'gpt-3.5-turbo' },
        { value: 'gpt-4', label: 'gpt-4' },
        { value: 'gpt-4o-mini', label: 'gpt-4o-mini' }
      ],
      form: {
        file: null,
        modelName: 'gpt-3.5-turbo'
      },
      uploadUrl: 'http://127.0.0.1:5000/api/translate'

    }
  },
  methods: {
    handleExceed(files, fileList) {
      this.$message.warning(`当前限制选择 1 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`);
    },
    handleFileChange(file) {
      this.form.file = file.raw; // 保存文件对象
    },
    handleError(err, file) {
      this.$message.error(`${file.name} 上传失败`);
    },
    async handleSubmit() {
      if (!this.form.file) {
        this.$message.warning('请先上传文件');
        return;
      }

      const formData = new FormData();
      formData.append('modelName', this.form.modelName);
      formData.append('file', this.form.file);

      try {
        const response = await fetch(this.uploadUrl, {
          method: 'POST',
          body: formData
        });
        const result = await response.json();
        console.log('提交成功:', result);
        this.$message.success('提交成功：'+result.result);
      } catch (error) {
        console.error('提交失败:', error);
        this.$message.error('提交失败');
      }
    }

  }
}
</script>

<style scoped>
#translate-page {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  margin-top: 30px;
  display: flex;
  flex-direction: column;
  align-items: center;  /* 水平居中 */
}
.el-row {
  margin-bottom: 20px;
}
</style>
