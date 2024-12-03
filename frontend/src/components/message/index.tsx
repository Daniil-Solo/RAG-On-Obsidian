import {MessageSchema} from "../../types/messages"
import Markdown from "react-markdown";
import remarkGfm from 'remark-gfm';
import {Prism as SyntaxHighlighter} from 'react-syntax-highlighter'
import {oneLight} from 'react-syntax-highlighter/dist/esm/styles/prism'
import "./index.css";

const MARKDOWN_STYLES = {
    code: ({...props}) => {
        const {children, className, node, ...rest} = props
        const match = /language-(\w+)/.exec(className || '')
        return match ? (
          <SyntaxHighlighter
            {...rest}
            PreTag="div"
            children={String(children).replace(/\n$/, '')}
            language={match[1]}
            style={oneLight}
          />
        ) : (
          <code {...rest} className={className}>
            {children}
          </code>
        )
      },
      h1: ({...props}) => <h1 style={{ fontSize: 28 }}>{props.children}</h1>,
      h2: ({...props}) => <h2 style={{ fontSize: 24 }}>{props.children}</h2>,
      h3: ({...props}) => <h3 style={{ fontSize: 20 }}>{props.children}</h3>,
      h4: ({...props}) => <h4 style={{ fontSize: 16 }}>{props.children}</h4>,
      p: ({...props}) => <p style={{ fontSize: 14 }}>{props.children}</p>,
      ol: ({...props}) => <ol style={{ listStyle: "auto", marginLeft: "32px" }}>{props.children}</ol>,
      ul: ({...props}) => <ul style={{ listStyle: "initial", marginLeft: "32px" }}>{props.children}</ul>,
      table: ({...props}) => <table style={{ borderCollapse: 'collapse', width: '100%' }}>{props.children}</table>,
      th: ({...props}) => <th style={{ border: '1px solid black', padding: '8px' }}>{props.children}</th>,
      td: ({...props}) => <td style={{ border: '1px solid black', padding: '8px' }}>{props.children}</td>,
}


export interface MessageProps  {
    message: MessageSchema
}


const Message = (props: MessageProps) => {
    const className = `message ${props.message.role}-message`
    
    return (
        <div className={className}>
            <Markdown 
                remarkPlugins={[remarkGfm]} 
                children={props.message.content} 
                className="reactMarkDown"
                components={MARKDOWN_STYLES}
            />
        </div>
    );
}
export default Message;