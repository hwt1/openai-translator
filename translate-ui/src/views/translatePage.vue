<template>
  <div id="translate-page" v-loading="loading" element-loading-text="努力翻译中...">
    <h1>翻译页面</h1>
    <!-- 这里添加你的页面内容 -->
    <el-form :model="form" ref="translateForm" @submit.prevent="handleSubmit" style="width: 60%">

      <el-row :gutter="10">
        <el-col :span="8">
          <el-form-item label="选择翻译模型" prop="modelName">
            <el-select
                v-model="form.modelName"
                class="m-2"
                style="width: 200px">
              <el-option
                  v-for="item in modelNames"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
              />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="选择输出文件类型" prop="fileFormat">
            <el-select
                v-model="form.fileFormat"
                class="m-2"
                style="width: 200px">
              <el-option
                  v-for="item in fileFormats"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
              />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="选择翻译语言" prop="targetLanguage">
            <el-select
                v-model="form.targetLanguage"
                class="m-2"
                style="width: 200px">
              <el-option
                  v-for="item in targetLanguages"
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
          <el-form-item label="上传文件" prop="file">
            <el-upload
                ref="uploadRef"
                class="upload-demo"
                drag
                :auto-upload="false"
                accept=".pdf"
                :limit="1"
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
      <el-row>
        <el-col :span="6">
          <el-form-item>
            <el-button type="primary" @click="handleSubmit">提 交</el-button>
            <el-button type="info" @click="resetForm">重 置</el-button>
          </el-form-item>
        </el-col>
      </el-row>


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
      loading: false,
      modelNames: [
        { value: 'gpt-3.5-turbo', label: 'gpt-3.5-turbo' },
        { value: 'gpt-4', label: 'gpt-4' },
        { value: 'gpt-4o-mini', label: 'gpt-4o-mini' }
      ],
      fileFormats: [
        {value: 'pdf', label: 'pdf'},
        {value: 'markdown', label: 'markdown'},
      ],
      targetLanguages: [
        {value: '中文', label: '中文'},
        {value: '英文', label: '英文'},
        {value: '日语', label: '日语'},
        {value: '法语', label: '法语'},
        {value: '德语', label: '德语'},
        {value: '西班牙语', label: '西班牙语'}
      ],
      form: {
        file: null,
        modelName: 'gpt-3.5-turbo',
        fileFormat: 'pdf',
        targetLanguage: '中文',
      },
      uploadUrl: 'http://127.0.0.1:5000/api/translate',
      outFileUrl:null /* 翻译结果文件路径 */

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
      formData.append('fileFormat', this.form.fileFormat);
      formData.append('file', this.form.file);
      formData.append('targetLanguage', this.form.targetLanguage);

      try {
        this.loading = true;
        const response = await fetch(this.uploadUrl, {
          method: 'POST',
          body: formData
        });
        const result = await response.json();

        this.outFileUrl = result.outFileUrl;
        this.downloadFile(this.outFileUrl);
        console.log('提交成功:', result);
        this.$message.success('提交成功：'+result.status);
      } catch (error) {
        console.error('提交失败:', error);
        alert(error)
        this.$message.error('提交失败,'+error);
      }finally{
        this.form.file = null;
        this.loading = false;
        this.resetForm()
      }
    },
    downloadFile(fileUrl) {
      const a = document.createElement('a');
      a.href = fileUrl;
      a.download = fileUrl.split('/').pop(); // 替换为你想要的文件名
      a.click();
    },
    openFile(fileUrl) {
      const a = document.createElement('a');
      a.href = fileUrl;
      a.target = '_blank'; // 在新标签页中打开
      a.click();
    },
    resetForm() {
      this.form.file = null;
      this.$refs.uploadRef.clearFiles(); // 清空文件上传组件
      this.$refs.translateForm.resetFields();
    }

  }
}
</script>

<style scoped>
#translate-page {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;  /* 水平居中 */
}
.el-row {
  margin-bottom: 20px;
}
</style>
