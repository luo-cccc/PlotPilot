<template>
  <div class="chapter-status-panel">
    <n-empty v-if="!chapter" description="请从左侧选择一个章节" style="margin-top: 48px" />

    <n-space v-else vertical :size="16" style="width: 100%; padding: 8px 4px">
      <n-card title="本章概览" size="small" :bordered="false">
        <n-descriptions :column="1" label-placement="left" size="small">
          <n-descriptions-item label="章节号">第 {{ chapter.number }} 章</n-descriptions-item>
          <n-descriptions-item label="标题">{{ chapter.title || '（无标题）' }}</n-descriptions-item>
          <n-descriptions-item label="收稿状态">
            <n-tag :type="chapter.word_count > 0 ? 'success' : 'default'" size="small" round>
              {{ chapter.word_count > 0 ? '已收稿' : '未收稿' }}
            </n-tag>
          </n-descriptions-item>
          <n-descriptions-item label="正文字数">{{ chapter.word_count ?? 0 }} 字</n-descriptions-item>
        </n-descriptions>
      </n-card>

      <n-alert v-if="readOnly" type="warning" :show-icon="true" title="托管运行中">
        全托管正在执行时，辅助撰稿区仅可阅读正文与关联信息，无法保存或改稿。请停止托管后再编辑。
      </n-alert>

      <n-text v-else depth="3" style="font-size: 12px">
        此处汇总当前章在结构中的基本状态；细粒度张力、文风等请在中栏「托管撰稿」下的监控大盘查看。
      </n-text>

      <n-card
        v-if="lastWorkflowResult && qcChapterNumber != null"
        title="AI 生成质检"
        size="small"
        :bordered="false"
      >
        <n-space vertical :size="12">
          <n-alert
            v-if="chapter.number !== qcChapterNumber"
            type="info"
            :show-icon="true"
            style="font-size: 12px"
          >
            以下结果为最近一次针对「第 {{ qcChapterNumber }} 章」流式生成的质检摘要；当前浏览为第
            {{ chapter.number }} 章。切换到第 {{ qcChapterNumber }} 章可对照正文。
          </n-alert>

          <ConsistencyReportPanel
            :report="lastWorkflowResult.consistency_report"
            :token-count="lastWorkflowResult.token_count"
            @location-click="onLocationClick"
          />

          <n-collapse
            v-if="
              lastWorkflowResult.style_warnings && lastWorkflowResult.style_warnings.length > 0
            "
            class="cliche-collapse"
          >
            <n-collapse-item
              :title="`俗套句式命中 ${lastWorkflowResult.style_warnings.length} 处（点击展开）`"
              name="cliche"
            >
              <n-space vertical :size="6">
                <n-alert
                  v-for="(w, i) in lastWorkflowResult.style_warnings"
                  :key="i"
                  :type="w.severity === 'warning' ? 'warning' : 'info'"
                  :title="w.pattern"
                  style="font-size: 12px"
                >
                  「{{ w.text }}」
                </n-alert>
              </n-space>
            </n-collapse-item>
          </n-collapse>

          <n-space :size="8" wrap>
            <n-button size="small" quaternary @click="$emit('go-editor')">打开章节编辑</n-button>
            <n-button size="small" quaternary @click="$emit('clear-qc')">清除质检摘要</n-button>
          </n-space>
        </n-space>
      </n-card>
    </n-space>
  </div>
</template>

<script setup lang="ts">
import { useMessage } from 'naive-ui'
import type { GenerateChapterWorkflowResponse } from '../../api/workflow'
import ConsistencyReportPanel from './ConsistencyReportPanel.vue'

interface Chapter {
  id: number
  number: number
  title: string
  word_count: number
}

defineProps<{
  chapter: Chapter | null
  readOnly?: boolean
  lastWorkflowResult?: GenerateChapterWorkflowResponse | null
  qcChapterNumber?: number | null
}>()

defineEmits<{
  (e: 'clear-qc'): void
  (e: 'go-editor'): void
}>()

const message = useMessage()

function onLocationClick(location: number) {
  message.info(`问题位置约在第 ${location} 字附近，可在章节编辑中搜索或滚动查看。`)
}
</script>

<style scoped>
.chapter-status-panel {
  height: 100%;
  min-height: 0;
  overflow-y: auto;
  padding: 12px 20px 20px;
}

.cliche-collapse :deep(.n-collapse-item__header) {
  font-size: 13px;
}
</style>
