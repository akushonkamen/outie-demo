App({
  onLaunch() {
    // [DEV PROBE] 域名过期开发期连通性探针（上线前删除）
    wx.request({
      url: this.apiBase + '/outie/event/current',
      method: 'GET',
      success: r => console.log('[PROBE] backend OK', r.statusCode),
      fail: e => console.log('[PROBE] backend FAIL', e && e.errMsg)
    });

    // 2026-10 域名过期临时方案：开发期直连服务器 IP。
// 开发者工具需勾选「详情→本地设置→不校验合法域名…」。域名恢复后改回：
// this.apiBase = 'https://www.our-verse.com/api';
this.apiBase = 'https://150.109.197.231/api';
    try { this.anonymousId = wx.getStorageSync('anonymousId') || ''; } catch (e) { this.anonymousId = ''; }
  }
});
