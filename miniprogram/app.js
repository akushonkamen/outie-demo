App({
  onLaunch() {
    // 域名已续费恢复（2026-10）。如再遇域名问题，临时直连 https://150.109.197.231/api（开发者工具需关 urlCheck）。
    this.apiBase = 'https://www.our-verse.com/api';
    // [DEV PROBE] 域名过期开发期连通性探针（上线前删除）
    wx.request({
      url: this.apiBase + '/outie/event/current',
      method: 'GET',
      success: r => console.log('[PROBE] backend OK', r.statusCode),
      fail: e => console.log('[PROBE] backend FAIL', e && e.errMsg)
    });
    try { this.anonymousId = wx.getStorageSync('anonymousId') || ''; } catch (e) { this.anonymousId = ''; }
  }
});
