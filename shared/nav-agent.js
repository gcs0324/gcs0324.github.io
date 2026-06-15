(function(){
  var pages=[
    {href:'agent-outline.html',label:'导航'},
    {href:'agent-01-tokenization.html',label:'01 Tokenization'},
    {href:'agent-02-rag.html',label:'02 RAG'},
    {href:'agent-03-prompt-engineering.html',label:'03 Prompt'},
    {href:'agent-04-context-engineering.html',label:'04 Context'},
    {href:'agent-05-model-routing.html',label:'05 路由'},
    {href:'agent-06-streaming.html',label:'06 流式'},
    {href:'agent-07-hallucination.html',label:'07 幻觉'},
    {href:'agent-08-finetuning.html',label:'08 微调'},
    {href:'agent-09-arch-patterns.html',label:'09 架构模式'},
    {href:'agent-10-langchain4j.html',label:'10 LangChain4j'},
    {href:'agent-11-spring-ai.html',label:'11 Spring AI'},
    {href:'agent-12-tool-calling.html',label:'12 Tool Calling'},
    {href:'agent-13-memory.html',label:'13 记忆'},
    {href:'agent-14-state-management.html',label:'14 状态管理'},
    {href:'agent-15-structured-output.html',label:'15 结构化输出'},
    {href:'agent-16-vector-db.html',label:'16 向量数据库'},
    {href:'agent-17-embedding.html',label:'17 Embedding'},
    {href:'agent-18-retrieval.html',label:'18 检索'},
    {href:'agent-19-cache-strategy.html',label:'19 缓存'},
    {href:'agent-20-observability.html',label:'20 可观测'},
    {href:'agent-21-multi-agent.html',label:'21 多Agent'},
    {href:'agent-22-evaluation.html',label:'22 评估'},
    {href:'agent-23-security.html',label:'23 安全'},
    {href:'agent-24-cost-control.html',label:'24 成本'},
    {href:'agent-25-cicd.html',label:'25 CI/CD'},
    {href:'agent-26-system-design.html',label:'26 系统设计'},
    {href:'agent-27-streaming-concurrency.html',label:'27 流式并发'},
    {href:'agent-28-event-driven.html',label:'28 事件驱动'},
    {href:'agent-29-interview.html',label:'29 面试题'}
  ];
  var cur=location.pathname.split('/').pop();
  var links=pages.map(function(p){return '<a href="'+p.href+'"'+(cur===p.href?' class="active"':'')+'>'+p.label+'</a>';}).join('');
  var nav='<div class="topnav"><a class="topnav-brand" href="agent-outline.html">Agent ·</a><div class="topnav-links">'+links+'</div></div>';
  document.currentScript.insertAdjacentHTML('afterend',nav);
})();
