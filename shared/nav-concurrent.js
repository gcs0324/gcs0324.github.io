(function(){
  var pages=[
    {href:'concurrent-outline.html',label:'导航'},
    {href:'concurrent-01-jmm.html',label:'01 JMM'},
    {href:'concurrent-02-thread.html',label:'02 线程'},
    {href:'concurrent-03-lock.html',label:'03 锁'},
    {href:'concurrent-04-juc.html',label:'04 JUC'},
    {href:'concurrent-05-pool.html',label:'05 线程池'},
    {href:'concurrent-06-interview.html',label:'06 面试题'}
  ];
  var cur=location.pathname.split('/').pop();
  var links=pages.map(function(p){return '<a href="'+p.href+'"'+(cur===p.href?' class="active"':'')+'>'+p.label+'</a>';}).join('');
  var nav='<div class="topnav"><a class="topnav-brand" href="concurrent-outline.html">并发 ·</a><div class="topnav-links">'+links+'</div></div>';
  document.currentScript.insertAdjacentHTML('afterend',nav);
})();
