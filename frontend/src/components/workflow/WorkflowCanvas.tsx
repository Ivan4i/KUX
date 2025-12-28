import { useCallback, useState } from 'react'
import ReactFlow, {
  Node,
  Edge,
  Controls,
  Background,
  MiniMap,
  addEdge,
  Connection,
  useNodesState,
  useEdgesState,
  NodeTypes,
  BackgroundVariant,
  Panel,
} from 'reactflow'
import 'reactflow/dist/style.css'
import { RiSaveLine, RiPlayLine, RiDeleteBinLine } from '@remixicon/react'

import { TriggerNode } from './nodes/TriggerNode'
import { ActionNode } from './nodes/ActionNode'
import { ConditionNode } from './nodes/ConditionNode'
import { NodePalette } from './NodePalette'

// Define node types
const nodeTypes: NodeTypes = {
  trigger: TriggerNode,
  action: ActionNode,
  condition: ConditionNode,
}

// Initial nodes for demo
const initialNodes: Node[] = [
  {
    id: 'trigger-1',
    type: 'trigger',
    position: { x: 250, y: 50 },
    data: {
      label: 'Fetch from Notion',
      description: 'Get pending leads',
      icon: 'notion',
    },
  },
  {
    id: 'action-1',
    type: 'action',
    position: { x: 250, y: 180 },
    data: {
      label: 'Analyze with Gemini',
      description: 'Generate personalized message',
      icon: 'gemini',
      agent: 'gemini',
    },
  },
  {
    id: 'condition-1',
    type: 'condition',
    position: { x: 250, y: 320 },
    data: {
      label: 'Has Phone?',
      description: 'Check if lead has phone number',
      condition: 'lead.phone != null',
    },
  },
  {
    id: 'action-2',
    type: 'action',
    position: { x: 100, y: 460 },
    data: {
      label: 'Send WhatsApp',
      description: 'Send message via WhatsApp',
      icon: 'whatsapp',
      agent: 'whatsapp',
    },
  },
  {
    id: 'action-3',
    type: 'action',
    position: { x: 400, y: 460 },
    data: {
      label: 'Send SMS',
      description: 'Send message via SMS',
      icon: 'sms',
      agent: 'sms',
    },
  },
]

// Initial edges
const initialEdges: Edge[] = [
  {
    id: 'e1-2',
    source: 'trigger-1',
    target: 'action-1',
    animated: true,
  },
  {
    id: 'e2-3',
    source: 'action-1',
    target: 'condition-1',
  },
  {
    id: 'e3-4',
    source: 'condition-1',
    target: 'action-2',
    sourceHandle: 'yes',
    label: 'Yes',
    style: { stroke: '#10b981' },
  },
  {
    id: 'e3-5',
    source: 'condition-1',
    target: 'action-3',
    sourceHandle: 'no',
    label: 'No',
    style: { stroke: '#ef4444' },
  },
]

interface WorkflowCanvasProps {
  scenarioId?: string
  onSave?: (nodes: Node[], edges: Edge[]) => void
  onRun?: () => void
}

export function WorkflowCanvas({ scenarioId: _scenarioId, onSave, onRun }: WorkflowCanvasProps) {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes)
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges)
  const [selectedNodes, setSelectedNodes] = useState<string[]>([])

  // Handle new connections
  const onConnect = useCallback(
    (params: Connection) => {
      setEdges((eds) => addEdge({ ...params, animated: true }, eds))
    },
    [setEdges]
  )

  // Handle node selection
  const onSelectionChange = useCallback(
    ({ nodes: selectedNodes }: { nodes: Node[] }) => {
      setSelectedNodes(selectedNodes.map((n) => n.id))
    },
    []
  )

  // Handle drop from palette
  const onDrop = useCallback(
    (event: React.DragEvent) => {
      event.preventDefault()

      const type = event.dataTransfer.getData('application/reactflow')
      const nodeData = JSON.parse(event.dataTransfer.getData('application/nodedata'))

      if (!type) return

      const position = {
        x: event.clientX - 250,
        y: event.clientY - 100,
      }

      const newNode: Node = {
        id: `${type}-${Date.now()}`,
        type,
        position,
        data: nodeData,
      }

      setNodes((nds) => [...nds, newNode])
    },
    [setNodes]
  )

  const onDragOver = useCallback((event: React.DragEvent) => {
    event.preventDefault()
    event.dataTransfer.dropEffect = 'move'
  }, [])

  // Delete selected nodes
  const deleteSelected = useCallback(() => {
    setNodes((nds) => nds.filter((n) => !selectedNodes.includes(n.id)))
    setEdges((eds) => eds.filter((e) =>
      !selectedNodes.includes(e.source) && !selectedNodes.includes(e.target)
    ))
    setSelectedNodes([])
  }, [selectedNodes, setNodes, setEdges])

  // Save workflow
  const handleSave = useCallback(() => {
    if (onSave) {
      onSave(nodes, edges)
    }
    console.log('Saving workflow:', { nodes, edges })
  }, [nodes, edges, onSave])

  // Run workflow
  const handleRun = useCallback(() => {
    if (onRun) {
      onRun()
    }
    console.log('Running workflow')
  }, [onRun])

  return (
    <div className="flex h-[calc(100vh-200px)] bg-gray-50 rounded-lg border border-gray-200 overflow-hidden">
      {/* Node Palette Sidebar */}
      <NodePalette />

      {/* Canvas */}
      <div className="flex-1" onDrop={onDrop} onDragOver={onDragOver}>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          onSelectionChange={onSelectionChange}
          nodeTypes={nodeTypes}
          fitView
          snapToGrid
          snapGrid={[15, 15]}
          defaultEdgeOptions={{
            style: { strokeWidth: 2, stroke: '#94a3b8' },
            type: 'smoothstep',
          }}
        >
          <Controls />
          <MiniMap
            nodeColor={(node) => {
              switch (node.type) {
                case 'trigger': return '#8b5cf6'
                case 'action': return '#3b82f6'
                case 'condition': return '#f59e0b'
                default: return '#94a3b8'
              }
            }}
            maskColor="rgba(0, 0, 0, 0.1)"
          />
          <Background variant={BackgroundVariant.Dots} gap={20} size={1} />

          {/* Top Panel with Actions */}
          <Panel position="top-right" className="flex gap-2">
            {selectedNodes.length > 0 && (
              <button
                onClick={deleteSelected}
                className="flex items-center gap-2 px-3 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors text-sm"
              >
                <RiDeleteBinLine className="size-4" />
                Delete ({selectedNodes.length})
              </button>
            )}
            <button
              onClick={handleSave}
              className="flex items-center gap-2 px-3 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-700 transition-colors text-sm"
            >
              <RiSaveLine className="size-4" />
              Save
            </button>
            <button
              onClick={handleRun}
              className="flex items-center gap-2 px-3 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm"
            >
              <RiPlayLine className="size-4" />
              Run
            </button>
          </Panel>
        </ReactFlow>
      </div>
    </div>
  )
}
