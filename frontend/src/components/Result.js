import React from 'react';

function Result({data}) {
        const {
                queryDto, metaInfo, baziElements
        } = data;
        return (
            <div>
                    <p>命主: {queryDto.name}（{queryDto.gender}）</p>
                    <p>生日: {queryDto.selfBirthday}</p>
                    {queryDto.partnerBirthday && <p>配偶生日: {queryDto.partnerBirthday}</p>} {/* 条件渲染配偶生日 */}
                    {queryDto.marriageDate && (
                        <p>结婚日期: {queryDto.marriageDate}{queryDto.isBridegroom && '（入赘）'}</p>
                    )}
                    {queryDto.addDetails && <p>添加更多解释</p>}
                    <p>开启功能列表: {queryDto.enabledFeatures.join(', ')}</p>

                    <h2>断命：</h2>
                    <p>农历生日: {metaInfo.lunar_birthday}</p>
                    <p>农历生日时辰: {metaInfo.lunar_birthday_hour}</p>
                    <p>八字: {metaInfo.bazi}</p>
                    <p>生肖: {metaInfo.zodiac}（{metaInfo.zodiac_cn}）</p>
                    <div>
                            <div className="flex-container">
                                    <div className="flex-item"><strong>时间</strong></div>
                                    <div className="flex-item"><strong>年柱</strong></div>
                                    <div className="flex-item"><strong>月柱</strong></div>
                                    <div className="flex-item"><strong>日柱</strong></div>
                                    <div className="flex-item"><strong>时柱</strong></div>
                            </div>
                            <div className="flex-container">
                                    <div className="flex-item"><strong>天干</strong></div>
                                    <div className="flex-item">{metaInfo.year_gan} ({metaInfo.year_gan_element})</div>
                                    <div className="flex-item">{metaInfo.month_gan} ({metaInfo.month_gan_element})</div>
                                    <div className="flex-item">{metaInfo.day_gan} ({metaInfo.day_gan_element})</div>
                                    <div className="flex-item">{metaInfo.hour_gan} ({metaInfo.hour_gan_element})</div>
                            </div>
                            <div className="flex-container">
                                    <div className="flex-item"><strong>地支</strong></div>
                                    <div className="flex-item">{metaInfo.year_zhi} ({metaInfo.year_zhi_element})</div>
                                    <div className="flex-item">{metaInfo.month_zhi} ({metaInfo.month_zhi_element})</div>
                                    <div className="flex-item">{metaInfo.day_zhi} ({metaInfo.day_zhi_element})</div>
                                    <div className="flex-item">{metaInfo.hour_zhi} ({metaInfo.hour_zhi_element})</div>
                            </div>
                    </div>

                    <h3>BaZi Elements</h3>
                    <p>是否强: {baziElements.isStrong ? '是' : '否'}</p>
                    <p>是否正: {baziElements.isPositive ? '是' : '否'}</p>
                    <p>支持元素: {baziElements.supportingElements.join(', ')}</p>
                    <p>反对元素: {baziElements.opposingElements.join(', ')}</p>
                    <h4>元素影响:</h4>
                    <ul>
                            {Object.entries(baziElements.elementsInfluence).map(([key, value]) => (
                                <li key={key}>{key}: {value}</li>
                            ))}
                    </ul>
                    <h4>元素影响权重:</h4>
                    <ul>
                            {Object.entries(baziElements.elementsInfluenceWeight).map(([key, value]) => (
                                <li key={key}>{key}: {value}</li>
                            ))}
                    </ul>
            </div>
        );
}

export default Result;
