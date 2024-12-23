const MANTINE_COLORS = [
    'red',
    'orange',
    'yellow',
    'green',
    'blue',
    'cyan',
    'indigo',
    'violet',
    'grape',
    'pink',
    'lime',
    'teal',
    'gray',
];

const getRandomInt = (min: number, max: number): number => {
    return Math.floor(Math.random() * (max - min + 1)) + min;
};


const getRandomColorAndNumber = (): string => {
    const randomColor = MANTINE_COLORS[getRandomInt(0, MANTINE_COLORS.length - 1)];
    const randomNumber = getRandomInt(2, 9);
    return `${randomColor}.${randomNumber}`
};

export {getRandomColorAndNumber}