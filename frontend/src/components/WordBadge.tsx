interface WordBadgeProps {
  word: string;
  tone: "fresh" | "rotten";
}

const WordBadge = ({ word, tone }: WordBadgeProps) => {
  return <span className={`word-badge ${tone}`}>{word}</span>;
};

export default WordBadge;
