# 71_VISUAL_WORKFLOW_BUILDER.md

## Visual Workflow Builder (Drag & Drop)

### Workflow Canvas Component

```typescript
// src/components/WorkflowBuilder/CanvasEditor.tsx
import React, { useState, useCallback } from 'react'
import ReactFlow, {
  Node,
  Edge,
  addEdge,
  Connection,
  useNodesState,
  useEdgesState,
  Background,
  Controls,
  MiniMap,
} from 'reactflow'
import 'reactflow/dist/style.css'

const initialNodes: Node[] = [
  {
    id: '1',
    data: { label: 'Start' },
    position: { x: 250, y: 5 },
    type: 'input',
  },
  {
    id: '2',
    data: { label: 'Open App' },
    position: { x: 100, y: 100 },
    type: 'default',
  },
  {
    id: '3',
    data: { label: 'Send Message' },
    position: { x: 250, y: 100 },
    type: 'default',
  },
  {
    id: '4',
    data: { label: 'End' },
    position: { x: 250, y: 200 },
    type: 'output',
  },
]

const initialEdges: Edge[] = [
  { id: 'e1-2', source: '1', target: '2' },
  { id: 'e1-3', source: '1', target: '3' },
  { id: 'e2-4', source: '2', target: '4' },
  { id: 'e3-4', source: '3', target: '4' },
]

export default function CanvasEditor() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes)
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges)
  const [selectedNode, setSelectedNode] = useState<Node | null>(null)
  
  const onConnect = useCallback(
    (connection: Connection) =>
      setEdges((eds) => addEdge(connection, eds)),
    [setEdges]
  )
  
  const onNodeClick = useCallback(
    (event: React.MouseEvent, node: Node) => {
      setSelectedNode(node)
    },
    []
  )
  
  const addNode = useCallback((type: string) => {
    const newNode: Node = {
      id: `node-${Date.now()}`,
      data: { label: type },
      position: { x: Math.random() * 400, y: Math.random() * 400 },
      type: 'default',
    }
    setNodes((nds) => nds.concat(newNode))
  }, [setNodes])
  
  const deleteNode = useCallback(() => {
    if (selectedNode) {
      setNodes((nds) => nds.filter((n) => n.id !== selectedNode.id))
      setEdges((eds) =>
        eds.filter((e) => e.source !== selectedNode.id && e.target !== selectedNode.id)
      )
      setSelectedNode(null)
    }
  }, [selectedNode, setNodes, setEdges])
  
  return (
    <div className="w-full h-full flex gap-4">
      {/* Canvas */}
      <div className="flex-1">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          onNodeClick={onNodeClick}
          fitView
        >
          <Background />
          <Controls />
          <MiniMap />
        </ReactFlow>
      </div>
      
      {/* Node Palette & Properties */}
      <div className="w-64 border-l border-gray-200 p-4 space-y-4">
        {/* Node Types */}
        <div>
          <h3 className="font-semibold mb-2">Add Node</h3>
          <div className="space-y-2">
            <button
              onClick={() => addNode('Open App')}
              className="w-full px-3 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
              + App
            </button>
            <button
              onClick={() => addNode('Click')}
              className="w-full px-3 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
              + Click
            </button>
            <button
              onClick={() => addNode('Type Text')}
              className="w-full px-3 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
              + Type
            </button>
            <button
              onClick={() => addNode('Wait')}
              className="w-full px-3 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
              + Wait
            </button>
            <button
              onClick={() => addNode('Check')}
              className="w-full px-3 py-2 bg-green-500 text-white rounded hover:bg-green-600"
            >
              + Condition
            </button>
          </div>
        </div>
        
        {/* Selected Node Properties */}
        {selectedNode && (
          <div className="border-t pt-4">
            <h3 className="font-semibold mb-2">Properties</h3>
            <div className="space-y-2">
              <div>
                <label className="text-sm font-medium">Label</label>
                <input
                  type="text"
                  defaultValue={selectedNode.data.label}
                  className="w-full px-2 py-1 border rounded"
                />
              </div>
              <button
                onClick={deleteNode}
                className="w-full px-3 py-2 bg-red-500 text-white rounded hover:bg-red-600"
              >
                Delete
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
```

### Custom Node Types

```typescript
// src/components/WorkflowBuilder/CustomNodes.tsx
import { Handle, Position } from 'reactflow'

export function AppNode({ data }) {
  return (
    <div className="px-4 py-2 shadow-lg rounded-lg bg-blue-50 border-2 border-blue-500">
      <div className="text-center font-semibold text-blue-900">{data.label}</div>
      <Handle type="target" position={Position.Top} />
      <Handle type="source" position={Position.Bottom} />
    </div>
  )
}

export function ActionNode({ data }) {
  return (
    <div className="px-4 py-2 shadow-lg rounded-lg bg-green-50 border-2 border-green-500">
      <div className="text-center font-semibold text-green-900">{data.label}</div>
      <Handle type="target" position={Position.Top} />
      <Handle type="source" position={Position.Bottom} />
    </div>
  )
}

export function ConditionNode({ data }) {
  return (
    <div className="px-4 py-2 shadow-lg rounded-lg bg-yellow-50 border-2 border-yellow-500">
      <div className="text-center font-semibold text-yellow-900">{data.label}</div>
      <Handle type="target" position={Position.Top} />
      <Handle type="source" position={Position.Bottom} label="Yes" />
      <Handle type="source" position={Position.Right} label="No" />
    </div>
  )
}
```

### Workflow Execution Engine

```typescript
// src/services/workflowExecutor.ts
import { Workflow, WorkflowNode, WorkflowEdge } from '../types/workflow'

class WorkflowExecutor {
  private workflow: Workflow
  private currentNodeId: string
  private context: Record<string, any> = {}
  
  constructor(workflow: Workflow) {
    this.workflow = workflow
    this.currentNodeId = this.workflow.nodes.find(n => n.type === 'start')?.id || ''
  }
  
  async execute(deviceId: string) {
    console.log(`🚀 Executing workflow on ${deviceId}`)
    
    while (true) {
      const currentNode = this.workflow.nodes.find(n => n.id === this.currentNodeId)
      if (!currentNode) break
      
      if (currentNode.type === 'end') {
        console.log('✅ Workflow completed')
        return true
      }
      
      // Execute node
      try {
        await this.executeNode(currentNode, deviceId)
      } catch (error) {
        console.error(`❌ Node failed: ${currentNode.label}`, error)
        return false
      }
      
      // Move to next node
      const nextEdge = this.workflow.edges.find(e => e.source === this.currentNodeId)
      if (!nextEdge) break
      
      this.currentNodeId = nextEdge.target
    }
    
    return true
  }
  
  private async executeNode(node: WorkflowNode, deviceId: string) {
    console.log(`→ Executing: ${node.label}`)
    
    switch (node.type) {
      case 'action':
        return await this.executeAction(node.data, deviceId)
      case 'condition':
        return await this.evaluateCondition(node.data, deviceId)
      default:
        return true
    }
  }
  
  private async executeAction(data: Record<string, any>, deviceId: string) {
    const { actionType, params } = data
    
    // Call backend API to execute action
    const response = await fetch('/api/execute-action', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        deviceId,
        actionType,
        params,
      })
    })
    
    if (!response.ok) {
      throw new Error(`Action failed: ${response.statusText}`)
    }
    
    return response.json()
  }
  
  private async evaluateCondition(data: Record<string, any>, deviceId: string) {
    // Similar to action, but evaluates condition
    const { conditionType, params } = data
    
    const response = await fetch('/api/evaluate-condition', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        deviceId,
        conditionType,
        params,
      })
    })
    
    const result = await response.json()
    
    // Update edge based on result
    if (result.value) {
      // Take "yes" path
      this.currentNodeId = this.workflow.edges
        .find(e => e.source === this.currentNodeId && e.label === 'yes')
        ?.target || ''
    } else {
      // Take "no" path
      this.currentNodeId = this.workflow.edges
        .find(e => e.source === this.currentNodeId && e.label === 'no')
        ?.target || ''
    }
    
    return true
  }
}

export { WorkflowExecutor }
```

### Workflow List & Management

```typescript
// src/pages/WorkflowsPage.tsx
import React, { useEffect, useState } from 'react'
import { Workflow } from '../types/workflow'

export default function WorkflowsPage() {
  const [workflows, setWorkflows] = useState<Workflow[]>([])
  const [loading, setLoading] = useState(true)
  
  useEffect(() => {
    fetchWorkflows()
  }, [])
  
  const fetchWorkflows = async () => {
    const response = await fetch('/api/workflows')
    const data = await response.json()
    setWorkflows(data)
    setLoading(false)
  }
  
  const createWorkflow = async () => {
    const name = prompt('Workflow name:')
    if (!name) return
    
    const response = await fetch('/api/workflows', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, description: '' })
    })
    
    const newWorkflow = await response.json()
    setWorkflows([...workflows, newWorkflow])
  }
  
  const deleteWorkflow = async (id: string) => {
    await fetch(`/api/workflows/${id}`, { method: 'DELETE' })
    setWorkflows(workflows.filter(w => w.id !== id))
  }
  
  if (loading) return <div>Loading...</div>
  
  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Workflows</h1>
        <button
          onClick={createWorkflow}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          + New Workflow
        </button>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {workflows.map(workflow => (
          <div key={workflow.id} className="border rounded-lg p-4 hover:shadow-lg transition">
            <h3 className="font-semibold text-lg">{workflow.name}</h3>
            <p className="text-gray-600 text-sm">{workflow.description}</p>
            
            <div className="mt-4 space-y-2">
              <div className="text-sm">
                Success Rate: <span className="font-bold">{workflow.successRate}%</span>
              </div>
              <div className="text-sm">
                Total Runs: <span className="font-bold">{workflow.totalRuns}</span>
              </div>
            </div>
            
            <div className="mt-4 flex gap-2">
              <button className="flex-1 px-3 py-1 bg-blue-500 text-white text-sm rounded hover:bg-blue-600">
                Edit
              </button>
              <button
                onClick={() => deleteWorkflow(workflow.id)}
                className="flex-1 px-3 py-1 bg-red-500 text-white text-sm rounded hover:bg-red-600"
              >
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
```

---

## End of 71_VISUAL_WORKFLOW_BUILDER.md