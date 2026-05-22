(function(){
  var pages=[
    {href:'jvm-outline.html',label:'导航'},
    {href:'jvm-01-memory.html',label:'01 内存模型'},
    {href:'jvm-02-gc.html',label:'02 GC'},
    {href:'jvm-03-classload.html',label:'03 类加载'},
    {href:'jvm-04-interview.html',label:'04 面试题'}
  ];
  var cur=location.pathname.split('/').pop();
  var links=pages.map(function(p){return '<a href="'+p.href+'"'+(cur===p.href?' class="active"':'')+'>'+p.label+'</a>';}).join('');
  var nav='<div class="topnav"><a class="topnav-brand" href="jvm-outline.html">JVM ·</a><div class="topnav-links">'+links+'</div></div>';
  document.currentScript.insertAdjacentHTML('afterend',nav);
})();
