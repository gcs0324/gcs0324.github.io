(function(){
  var pages=[
    {href:'kafka-outline.html',label:'导航'},
    {href:'kafka-01-arch.html',label:'01 架构'},
    {href:'kafka-02-producer.html',label:'02 Producer'},
    {href:'kafka-03-consumer.html',label:'03 Consumer'},
    {href:'kafka-04-reliable.html',label:'04 可靠性'},
    {href:'kafka-05-spring.html',label:'05 Spring'},
    {href:'kafka-06-interview.html',label:'06 面试题'}
  ];
  var cur=location.pathname.split('/').pop();
  var links=pages.map(function(p){return '<a href="'+p.href+'"'+(cur===p.href?' class="active"':'')+'>'+p.label+'</a>';}).join('');
  var nav='<div class="topnav"><a class="topnav-brand" href="kafka-outline.html">Kafka ·</a><div class="topnav-links">'+links+'</div></div>';
  document.currentScript.insertAdjacentHTML('afterend',nav);
})();
