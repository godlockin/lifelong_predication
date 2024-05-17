import React, { useState, useEffect } from 'react';
import DatePicker from 'react-datepicker';
import Select from 'react-select';
import moment from 'moment-timezone';
import 'react-datepicker/dist/react-datepicker.css';

function Form({ onResult }) {
  const [name, setName] = useState('陈沐');
  const [selfBirthday, setSelfBirthday] = useState(moment().tz('Asia/Shanghai').toDate());
  const [gender, setGender] = useState('male');
  const [partnerBirthday, setPartnerBirthday] = useState(null);
  const [marriageDate, setMarriageDate] =useState(null);
  const [isBridegroom, setIsBridegroom] = useState(false);
  const [addDetails, setAddDetails] = useState(false);
  const [enabledFeatures, setEnabledFeatures] = useState([]);
  const [featuresOptions, setFeaturesOptions] = useState([]);

  useEffect(() => {
    // 从后端获取功能选项
    const fetchFeatures = async () => {
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/prediction/features`);
      const data = await response.json();
      const options = Object.keys(data).map(key => ({
        value: key,
        label: data[key]
      }));
      setFeaturesOptions(options);
    };
    fetchFeatures();
  }, []);

  const genderOptions = [
    { value: 'male', label: '男' },
    { value: 'female', label: '女' }
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formattedBirthdate = moment(selfBirthday).tz('Asia/Shanghai').format();
    const formattedPartnerBirthday = partnerBirthday ? moment(partnerBirthday).tz('Asia/Shanghai').format() : null;
    const formattedMarriageDate = marriageDate ? moment(marriageDate).tz('Asia/Shanghai').format() : null;

    const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/prediction/process/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name,
        selfBirthday: formattedBirthdate,
        gender,
        partnerBirthday: formattedPartnerBirthday,
        marriageDate: formattedMarriageDate,
        isBridegroom,
        addDetails,
        enabledFeatures,
      }),
    });
    const data = await response.json();
    onResult(data);
  };

  return (
      <form onSubmit={handleSubmit}>
        <div>
          <label>命主姓名:</label>
          <input
              type="text"
              value={name}
              onChange={e => setName(e.target.value)}
              required
          />
        </div>
        <div>
          <label>命主生日:</label>
          <DatePicker
              selected={selfBirthday}
              onChange={date => setSelfBirthday(date)}
              showTimeSelect
              timeFormat="HH:mm"
              timeIntervals={15}
              timeCaption="时间"
              dateFormat="yyyy/MM/dd HH:mm"
              required
          />
        </div>
        <div>
          <label>命主性别:</label>
          <Select
              options={genderOptions}
              value={genderOptions.find(option => option.value === gender)}
              onChange={option => setGender(option.value)}
          />
        </div>
        <div>
          <label>命主对象生日:</label>
          <DatePicker
              selected={partnerBirthday}
              onChange={date => setPartnerBirthday(date)}
              showTimeSelect
              timeFormat="HH:mm"
              timeIntervals={15}
              timeCaption="时间"
              dateFormat="yyyy/MM/dd HH:mm"
              isClearable
          />
        </div>
        <div>
          <label>结婚日期:</label>
          <DatePicker
              selected={marriageDate}
              onChange={date => setMarriageDate(date)}
              showTimeSelect
              timeFormat="HH:mm"
              timeIntervals={15}
              timeCaption="时间"
              dateFormat="yyyy/MM/dd HH:mm"
              isClearable
          />
        </div>
        <div>
          <label>
            <input
                type="checkbox"
                checked={isBridegroom}
                onChange={() => setIsBridegroom(!isBridegroom)}
            />
            命主婚姻是否存在入赘
          </label>
        </div>
        <div>
          <label>
            <input
                type="checkbox"
                checked={addDetails}
                onChange={() => setAddDetails(!addDetails)}
            />
            添加详情
          </label>
        </div>
        <div>
          <label>开启功能:</label>
          <Select
              options={featuresOptions}
              isMulti
              value={featuresOptions.filter(option => enabledFeatures.includes(option.value))}
              onChange={options => setEnabledFeatures(options.map(option => option.value))}
          />
        </div>
        <button type="submit">Submit</button>
      </form>
  );
}

export default Form;
